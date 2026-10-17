import hashlib
import hmac
import secrets
import sqlite3


class AuthError(Exception):
    """Ошибка, которую можно безопасно показать пользователю."""


class AuthService:
    ITERATIONS = 310_000
    MIN_PASSWORD_LENGTH = 8

    def __init__(self, database):
        self.db = database

    @classmethod
    def _hash_password(cls, password, salt_hex):
        return hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            cls.ITERATIONS,
        ).hex()

    @staticmethod
    def _validate_username(username):
        username = username.strip()
        if len(username) < 3 or len(username) > 32:
            raise AuthError("Логин должен содержать от 3 до 32 символов.")
        if not all(ch.isalnum() or ch in "._-" for ch in username):
            raise AuthError("В логине разрешены буквы, цифры, точка, дефис и подчёркивание.")
        return username

    @classmethod
    def _validate_password(cls, password):
        if len(password) < cls.MIN_PASSWORD_LENGTH:
            raise AuthError("Пароль должен содержать не менее 8 символов.")
        if len(password) > 256:
            raise AuthError("Пароль слишком длинный.")

    def register(self, username, password):
        username = self._validate_username(username)
        self._validate_password(password)

        if self.db.fetchone("SELECT id FROM users WHERE username = ?", (username,)):
            raise AuthError("Такой логин уже существует.")

        salt = secrets.token_hex(16)
        password_hash = self._hash_password(password, salt)
        role = "admin" if self.db.fetchone("SELECT id FROM users LIMIT 1") is None else "user"

        try:
            user_id = self.db.execute(
                """
                INSERT INTO users (username, password_hash, salt, role)
                VALUES (?, ?, ?, ?)
                """,
                (username, password_hash, salt, role),
            )
        except sqlite3.IntegrityError:
            raise AuthError("Такой логин уже существует.") from None

        return self.get_user(user_id)

    def login(self, username, password):
        username = username.strip()
        user = self.db.fetchone(
            "SELECT id, username, password_hash, salt, role, created_at "
            "FROM users WHERE username = ?",
            (username,),
        )
        if user is None:
            raise AuthError("Неверный логин или пароль.")

        candidate = self._hash_password(password, user["salt"])
        if not hmac.compare_digest(candidate, user["password_hash"]):
            raise AuthError("Неверный логин или пароль.")

        return self.get_user(user["id"])

    def get_user(self, user_id):
        user = self.db.fetchone(
            "SELECT id, username, role, created_at FROM users WHERE id = ?",
            (user_id,),
        )
        return dict(user) if user else None

    def list_users(self, actor):
        self._require_admin(actor)
        rows = self.db.fetchall(
            "SELECT id, username, role, created_at FROM users ORDER BY id"
        )
        return [dict(row) for row in rows]

    def set_role(self, actor, target_id, role):
        self._require_admin(actor)
        if role not in ("user", "admin"):
            raise AuthError("Неизвестная роль.")
        if actor["id"] == target_id and role != "admin":
            raise AuthError("Нельзя снять роль администратора с самого себя.")
        if role == "user":
            admins = self.db.fetchone("SELECT COUNT(*) AS count FROM users WHERE role = 'admin'")
            target = self.get_user(target_id)
            if target and target["role"] == "admin" and admins["count"] <= 1:
                raise AuthError("В системе должен остаться хотя бы один администратор.")
        self.db.execute("UPDATE users SET role = ? WHERE id = ?", (role, target_id))

    def delete_user(self, actor, target_id):
        self._require_admin(actor)
        if actor["id"] == target_id:
            raise AuthError("Нельзя удалить собственный аккаунт из этого окна.")
        target = self.get_user(target_id)
        if target is None:
            raise AuthError("Пользователь уже удалён.")
        if target["role"] == "admin":
            admins = self.db.fetchone("SELECT COUNT(*) AS count FROM users WHERE role = 'admin'")
            if admins["count"] <= 1:
                raise AuthError("Нельзя удалить последнего администратора.")
        self.db.execute("DELETE FROM users WHERE id = ?", (target_id,))

    def change_password(self, actor, old_password, new_password):
        self._validate_password(new_password)
        row = self.db.fetchone(
            "SELECT password_hash, salt FROM users WHERE id = ?", (actor["id"],)
        )
        if row is None:
            raise AuthError("Аккаунт не найден.")
        old_hash = self._hash_password(old_password, row["salt"])
        if not hmac.compare_digest(old_hash, row["password_hash"]):
            raise AuthError("Текущий пароль введён неверно.")
        salt = secrets.token_hex(16)
        password_hash = self._hash_password(new_password, salt)
        self.db.execute(
            "UPDATE users SET password_hash = ?, salt = ? WHERE id = ?",
            (password_hash, salt, actor["id"]),
        )

    @staticmethod
    def _require_admin(actor):
        if not actor or actor.get("role") != "admin":
            raise AuthError("Это действие доступно только администратору.")

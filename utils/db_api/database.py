from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        language VARCHAR(10)
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id, language='null'):
        sql = "INSERT INTO users (full_name, username, telegram_id, language) " \
              "VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, full_name, username, telegram_id, language, fetchrow=True)

    async def update_user_name(self, telegram_id, name):
        telegram_id = str(telegram_id)
        sql = f"UPDATE Users SET full_name='{name}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)


    async def isUser_subscribed(self, telegram_id):
        telegram_id = str(telegram_id)
        sql = f"SELECT is_subscribed FROM Users WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, fetchval=True)

    async def update_user_phone(self, telegram_id, phone):
        telegram_id = str(telegram_id)
        sql = f"UPDATE Users SET phone='{phone}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def getUser_name(self, telegram_id):
        telegram_id = str(telegram_id)
        sql = f"SELECT full_name FROM Users WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, fetchval=True)

    async def get_all_names(self):
        sql = f"SELECT full_name FROM Users"
        return await self.execute(sql, execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, telegram_id):
        sql = f"SELECT * FROM Users WHERE telegram_id = '{telegram_id}'"
        return await self.execute(sql, fetchrow=True)

    async def get_Users_username(self):
        sql = "SELECT telegram_id FROM Users"
        return await self.execute(sql, fetchrow=True)

    async def get_user_role(self, telegram_id):
        sql = f"SELECT role FROM Users WHERE telegram_id = '{telegram_id}'"
        return await self.execute(sql, fetchrow=True)
    
    async def getUser_lang(self, telegram_id):
        telegram_id = str(telegram_id)
        sql = f"SELECT language FROM Users WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, fetchval=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)
    
    async def update_user_language(self, telegram_id, lang):
        telegram_id = str(telegram_id)
        sql = f"UPDATE Users SET language='{lang}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def delete_user_by_id(self, telegram_id):
        await self.execute(f"DELETE FROM Users WHERE telegram_id = '{telegram_id}'", execute=True)

    async def delete_user(self, telegram_id):
        await self.execute(f"DELETE FROM Users WHERE telegram_id = '{telegram_id}'", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    #########################################################################

    async def create_table_test(self):
        sql = """
        CREATE TABLE IF NOT EXISTS TESTS (
        id SERIAL PRIMARY KEY,
        test_name VARCHAR(255) NOT NULL,
        test_id BIGINT, 
        answers VARCHAR(1000),
        len BIGINT,
        creator_id BIGINT NOT NULL,
        type VARCHAR (100),
        status INTEGER,
        created_time VARCHAR(40)
        );
        """

        await self.execute(sql, execute=True)

    async def add_test(self, test_name, test_id, answers, len, creator_id, type, status, created_time):
        sql = """
        INSERT INTO TESTS (test_name, test_id, answers, len, creator_id, type, status, created_time) VALUES ($1, $2, $3, $4, $5, $6, $7, $8) returning *
        """
        return await self.execute(sql, test_name, test_id, answers, len, creator_id, type, status, created_time, fetchrow=True)

    async def get_test_by_id(self, test_id):
        sql = f"""
        SELECT * FROM TESTS WHERE test_id = '{test_id}'
        """
        return await self.execute(sql, fetchrow=True)

    async def get_test_answers(self, test_id):
        sql = f"""
        SELECT answers FROM TESTS WHERE test_id = '{test_id}'
        """
        return await self.execute(sql, fetchval=True)

    async def get_test_type(self, test_id):
        sql = f"""
        SELECT type FROM TESTS WHERE test_id = '{test_id}'
        """
        return await self.execute(sql, fetchval=True)
    
    async def get_test_status(self, test_id):
        sql = f"""
        SELECT status FROM TESTS WHERE test_id = '{test_id}'
        """
        return await self.execute(sql, fetchval=True)
    
    async def update_test_status(self, test_id, status):
        sql = f"UPDATE Tests SET status='{status}' WHERE test_id='{test_id}'"
        return await self.execute(sql, execute=True)

    async def get_test_name(self, test_id):
        sql = f"""
        SELECT test_name FROM TESTS WHERE test_id = '{test_id}'
        """
        return await self.execute(sql, fetchval=True)
    
    async def get_test_by_creator(self, creator_id):
        sql = f"""
        SELECT test_id, created_time FROM TESTS WHERE creator_id = '{creator_id}' ORDER BY created_time DESC
        """
        return await self.execute(sql, fetch=True)
    
    async def get_test_creator(self, test_id):
        sql = f"""
        SELECT creator_id FROM TESTS WHERE test_id = '{test_id}'
        """
        return await self.execute(sql, fetchval=True)

    async def get_test_length(self, test_id):
        sql = f"""
        SELECT len FROM TESTS WHERE test_id = '{test_id}'
        """
        return await self.execute(sql, fetchval=True)
    
    async def get_test_date(self, test_id):
        sql = f"""
        SELECT created_time FROM TESTS WHERE test_id = '{test_id}'
        """
        return await self.execute(sql, fetchval=True)
    
    async def count_test(self):
        sql = "SELECT COUNT(*) FROM Tests"
        return await self.execute(sql, fetchval=True)

    async def drop_test(self):
        await self.execute("DROP TABLE TESTS", execute=True)

    # Mening testlarim



    async def create_table_done_test(self):
        sql = """
        CREATE TABLE IF NOT EXISTS DoneTests (
        id SERIAL PRIMARY KEY,
        test_id BIGINT NOT NULL,
        user_id BIGINT NOT NULL,
        created_time VARCHAR (255)
        );
        """

        await self.execute(sql, execute=True)

    async def add_done_test(self, test_id, user_id, created_time):
        sql = """
        INSERT INTO DoneTests (test_id, user_id, created_time) VALUES ($1, $2, $3) returning *
        """
        return await self.execute(sql, test_id, user_id, created_time, fetchrow=True)
    



    async def delete_done_test_by_user(self, tg_id):
        await self.execute(f"DELETE FROM DoneTests WHERE user_id = '{tg_id}'", execute=True)

    async def check_is_done(self, test_id, user_id):
        sql = f"""
        SELECT * FROM DoneTests WHERE user_id = '{user_id}' AND test_id = '{test_id}'
        """
        return await self.execute(sql, fetchrow=True)
    

    async def count_participants(self, test_id):
        sql = f"""
        SELECT COUNT(*) FROM DoneTests WHERE test_id = '{test_id}'
        """
        return await self.execute(sql, fetch=True)
    
    


    async def delete_done_test(self):
        await self.execute("DROP TABLE DoneTests", execute=True)

    async def create_table_rating(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Rating (
        id SERIAL PRIMARY KEY,
        test_id VARCHAR (255),
        user_id VARCHAR (255),
        full_name VARCHAR (255),
        ball FLOAT,
        created_time timestamp,
        type VARCHAR (255)
        );
        """

        await self.execute(sql, execute=True)

    async def add_rating(self, test_id, user_id, full_name, ball, created_time, type):
        sql = """
        INSERT INTO Rating (test_id, user_id, full_name, ball, created_time, type) VALUES ($1, $2, $3, $4, $5, $6) returning *
        """
        return await self.execute(sql, test_id, user_id, full_name, ball, created_time, type, fetchrow=True)

    async def show_rating_by_user(self, test_id):
        sql = f"""
        SELECT full_name, ball, created_time FROM Rating WHERE test_id='{test_id}' ORDER BY ball DESC, created_time ASC LIMIT 500
        """
        return await self.execute(sql, fetch=True)

    async def get_rating_ball(self, test_id):
        sql = f"""
        SELECT ball from Rating WHERE test_id = '{test_id}'
        """

    async def get_test_users(self, test_id):
        sql = f"""
        SELECT user_id FROM Rating WHERE test_id = '{test_id}'
        """
        return await self.execute(sql, fetch=True)

    async def delete_table_rating(self):
        await self.execute("DROP TABLE Rating", execute=True)



    async def create_table_errors(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Errors (
        id SERIAL PRIMARY KEY,
        test_id VARCHAR (255),
        user_id VARCHAR (255),
        errors INTEGER
        );
        """

        await self.execute(sql, execute=True)

    async def add_errors(self, user_id, test_id, error):
        sql = """
        INSERT INTO Errors (test_id, user_id, errors) VALUES ($1, $2, $3) returning *
        """
        return await self.execute(sql, test_id, user_id, error,  fetchrow=True)
    
    async def get_user_errors(self, user_id, test_id):
        sql = f"""
        SELECT errors FROM Errors WHERE test_id = '{test_id}' AND user_id = '{user_id}'
        """
        return await self.execute(sql, fetch=True)



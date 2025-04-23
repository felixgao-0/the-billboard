"""
Database for handling random things which need to be stored lol
"""
import time
from typing import Optional
from urllib.parse import quote_plus

import psycopg
from psycopg_pool import ConnectionPool


class Database:
    """
    It's... a database :3
    """
    def __init__(self, user: str, port: str, password: str, host: str, dbname: str) -> None:
        # note to self: url encode pw or else explosions and fire
        self.pool = ConnectionPool(
            f"postgresql://{user}:{quote_plus(password)}@{host}:{port}/{dbname}",
            min_size=1,
            max_size=10,
            max_lifetime=60*10 # 60 sec * 10 = 10 min
        )


    def get_ad(self, *, current_timestamp: Optional[int] = None, ad_url: Optional[str] = None, user_id: Optional[str] = None) -> list:
        """
        Yoinks an ad to shove in everyone's face against their will
        """
        if not ad_url and not current_timestamp and not user_id:
            raise ValueError("Either ad_url or current_timestamp must be provided bruh")
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                if ad_url:
                    cur.execute("""
                        SELECT * FROM ads
                        WHERE ad_img = %s;
                    """, (ad_url,)
                    )
                elif current_timestamp:
                    cur.execute("""
                        SELECT ads.* FROM ads
                        JOIN schedules ON ads.id = schedules.ad_id
                        WHERE %s BETWEEN schedules.start_epoch AND schedules.end_epoch;
                    """, (current_timestamp,)
                    )
                elif user_id:
                    cur.execute("""
                        SELECT * FROM ads
                        WHERE user_id = %s;
                    """, (user_id,)
                    )
                return cur.fetchall()


    def add_ad(self, slack_id: str, ad_text: str, ad_img: str, 
               ad_alt: str, ad_cta: str, *, status: str = 'PENDING') -> None:
        """
        Adds an ad to the database

        :param slack_id: Ad creator
        :param ad_text: The text of the ad
        :param ad_img: The ad image itself
        :param ad_alt: Ad alt text
        :param ad_cta: The call to action
        :param status: The status of the ad (default: PENDING)
        """
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        INSERT INTO ads (user_id, ad_text, ad_img, ad_alt, ad_cta, status)
                        VALUES  (%s, %s, %s, %s, %s, %s)""", (slack_id, ad_text, ad_img, ad_alt, ad_cta, status)
                    )
                except psycopg.errors.UniqueViolation:
                    raise ValueError("Ad already exists in the database") from None
                conn.commit()


    def change_ad_status(self, ad_id: int, status: str) -> None:
        """
        Set an ad's status to whatever

        :param ad_id: The ad ID to set
        """
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE ads
                    SET status = %s
                    WHERE id = %s;
                """, (status, ad_id))
                conn.commit()


    def add_schedule(self, ad_id: int, start_epoch: int, end_epoch: int) -> None:
        """
        Schedules an ad in the database
        """
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO schedules (ad_id, start_epoch, end_epoch)
                    VALUES  (%s, %s, %s)""", (ad_id, start_epoch, end_epoch)
                )
                conn.commit()

if __name__ == "__main__":
    import os

    db_conn_params = {
        "dbname": "felixgao_the_billboard",
        "user": "felixgao",
        "password": os.environ['DB_PASSWORD'],
        "host": "hackclub.app",
        "port": 5432
    }

    db = Database(**db_conn_params)

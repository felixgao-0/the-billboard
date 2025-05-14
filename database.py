"""
Database for handling random ad junk which needs to be stored lol

Yes I know a lot of this is jank, do let me know if you have a solution (please save me)
"""
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


    def get_ad(self, *, current_timestamp: Optional[int] = None,
               param: Optional[list[str, str]] = None, status: Optional[str] = None) -> list:
        """
        Yoinks an ad to shove in everyone's face against their will
        """
        if not current_timestamp and not param and not status: # permission, not forgiveness
            raise ValueError("One of these params must be provided bruh")
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                if param:
                    # !!!! README: THIS IS SAFE !!!!
                    # No user input controls param[0], so no risk of SQL injection
                    cur.execute(f"""
                        SELECT ads.*, approvals.status, approvals.objectable FROM ads
                        JOIN approvals ON approvals.ad_id = ads.id
                        WHERE ads.{param[0]} = %s
                        AND approvals.id = ( -- get the latest approval for this ad
                            SELECT MAX(approvals.id)
                            FROM approvals
                            WHERE ad_id = ads.id
                        );
                    """, (param[1],)
                    )
                elif current_timestamp:
                    cur.execute("""
                        SELECT ads.* FROM ads
                        JOIN schedules ON ads.id = schedules.ad_id
                        WHERE %s BETWEEN schedules.start_epoch AND schedules.end_epoch;
                    """, (current_timestamp,)
                    )
                elif status:
                    cur.execute("""
                        SELECT * FROM ads
                        WHERE EXISTS (
                            SELECT 1 FROM approvals a WHERE a.ad_id = ads.id
                            AND a.id = (SELECT MAX(id) FROM approvals WHERE ad_id = ads.id)
                            AND a.status = %s
                        );
                    """, (status,)) # check for staus = whatever
                return cur.fetchall()


    def get_ad_approvals(self, ad_id: int) -> list:
        """
        Gets the ad approvals for a specific ad
        """
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM approvals
                    WHERE ad_id = %s
                    ORDER BY id DESC;
                """, (ad_id,)
                )
                return cur.fetchall()


    def add_ad(self, slack_id: str, ad_text: str, ad_img: str, ad_alt: str, ad_cta: str) -> None:
        """
        Adds an ad to the database

        :param slack_id: Ad creator
        :param ad_text: The text of the ad
        :param ad_img: The ad image itself
        :param ad_alt: Ad alt text
        :param ad_cta: The call to action
        """
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        INSERT INTO ads (user_id, ad_text, ad_img, ad_alt, ad_cta)
                        VALUES  (%s, %s, %s, %s, %s)
                        RETURNING id""", (slack_id, ad_text, ad_img, ad_alt, ad_cta)
                    )
                except psycopg.errors.UniqueViolation:
                    raise ValueError("Ad already exists in the database") from None
                result = cur.fetchone()[0]
                conn.commit()
        return result

    def add_approval_setup(self, ad_id: int) -> None:
        """
        Hi I heard you wanted your ad approved!

        DOES NOT APPROVE THE AD, JUST SETS IT UP FOR APPROVAL
        :param ad_id: The ad ID to set as pending
        """
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO approvals (ad_id, status, reason, objectable)
                    VALUES  (%s, %s, %s, %s)""", (ad_id, "PENDING", "Ad uploaded.", True)
                )
                conn.commit()


    def add_ad_status(self, ad_id: int, status: str, reason="No reason provided.", objectable=True) -> None:
        """
        Set an ad's status to whatever

        :param ad_id: The ad ID to set
        """
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO approvals (ad_id, status, reason, objectable)
                    VALUES (%s, %s, %s, %s)""", (ad_id, status, reason, objectable)
                )
                conn.commit()


    def get_schedule(self, start_epoch: int, end_epoch: int) -> list:
        """
        Gets schedules during a time range (for scheduling mainly)
        """
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM schedules
                    WHERE start_epoch >= %s AND end_epoch <= %s;
                """, (start_epoch, end_epoch))
                return cur.fetchall()


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
    import datetime
    from dotenv import load_dotenv

    load_dotenv()


    db_conn_params = {
        "dbname": "felixgao_the_billboard",
        "user": "felixgao",
        "password": os.environ['DB_PASSWORD'],
        "host": "hackclub.app",
        "port": 5432
    }

    db = Database(**db_conn_params)
    e = db.get_ad(param=['id',10])
    # # 5 7 8 9
    # start = datetime.datetime.combine(datetime.datetime.today(), datetime.time(0,0))
    # end = datetime.datetime.combine(datetime.datetime.today(), datetime.time(10,0))

    # db.add_schedule(4, start.timestamp(), end.timestamp())
    print(e)

    db.pool.close()

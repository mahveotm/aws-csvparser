"""Marv, August 2021"""

import json
import os
import sys
import urllib.parse
import boto3
import csv
from datetime import datetime
import sqlite3

conn = sqlite3.connect("/mnt/access/entries.db")
c = conn.cursor()

s3 = boto3.client("s3")


def handler(event, context):
    # init_db()
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response["ContentType"])
        csvcontent = response["Body"].read().decode("utf-8").splitlines()
        proccess_csv(csvcontent)
        c.execute("SELECT * FROM db_entries")
        print(c.fetchall())

        return response["ContentType"]

    except Exception as e:
        print(e)
        print(
            f"Error getting object {key} from bucket {bucket}. Make sure they exist and your bucket is in the same region as this function."
        )
        raise e


def proccess_csv(csvcontent):
    data = csv.reader(csvcontent)
    # skip first entry that contains csv descriptions.
    next(data)
    # loop over, confirming that,
    for x in data:
        # the batch data consists of alphabet,
        if x[0].isalpha():
            # print(x[0])
            # the records entry is entirely made of numbers
            if x[3].isnumeric():
                # print(x[3])
                # convert the boolean entry to a uniform format and confirm column entry conforms
                if x[4].lower() == "true" or x[4].lower() == "false":
                    # print(x)
                    # attempt converting datetime entry to standardized datetime library. failing mean column entry is not a valid datetime.
                    try:
                        datetime.strptime(
                            x[2], "%Y-%m-%dT%H:%M:%S"
                        ) and datetime.strptime(x[1], "%Y-%m-%dT%H:%M:%S")
                        c.execute(
                            "INSERT INTO db_entries VALUES(?,?,?,?,?,?)", tuple(x)
                        )
                        conn.commit()
                        # print(x)
                    except Exception as e:
                        print("Invalid start/end date. Please reverify", x, e)
                else:
                    print("Not entered. Not a valid Boolean", x)
            else:
                print("Not entered. Entry not a valid numeric value", x)

        else:
            print("Not entered. Entry not an alphabeth", x)


def init_db():
    c = conn.cursor()
    c.execute(
        """CREATE TABLE db_entries (
        batch text,
        start datetime,
        end datetime,
        records integer,
        pass boolean,
        message text
        )"""
    )

    conn.commit()

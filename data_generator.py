import csv
import pandas as pd

from faker import Faker
from pydbgen import pydbgen
from random import randint

PERSON_COUNT = 10000
CORP_COUNT = 1000
PERSON_SHAREHOLD_COUNT = 20000
CORP_REL_COUNT = 100
CORP_SHAREHOLD_COUNT = 200
PERSON_REL_COUNT = 1000
PERSON_ROLE_COUNT = 5000

WRITE_BATCH = 1000


def csv_writer(file_path, row_count, row_generator):
    with open(file_path, mode='w') as file:
        writer = csv.writer(
            file, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
        csv_buffer = list()
        for row in range(row_count):
            csv_buffer.append(row_generator())
            if len(csv_buffer) > WRITE_BATCH:
                writer.writerows(csv_buffer)
                del csv_buffer[:]
        if csv_buffer:
            writer.writerows(csv_buffer)
            del csv_buffer[:]


generator = pydbgen.pydb()
faker = Faker()

# PERSON
person_df = generator.gen_dataframe(num=PERSON_COUNT, fields=['name'])
person_pd = pd.DataFrame(person_df)
person_pd = person_pd.set_index('p_' + person_pd.index.astype(str))
person_pd.to_csv('data/person.csv', header=False, quoting=csv.QUOTE_MINIMAL)

# CORP
corp_df = generator.gen_dataframe(num=CORP_COUNT, fields=['company'])
corp_pd = pd.DataFrame(corp_df)
corp_pd = corp_pd.set_index('c_' + corp_df.index.astype(str))
corp_pd.to_csv('data/corp.csv', header=False, quoting=csv.QUOTE_MINIMAL)


# PERSON SHAREHOLD RELATION
def person_share_generator():
    """
    (pid, cid, share)
    """
    return (
        'p_'+str(randint(0, PERSON_COUNT-1)),
        'c_'+str(randint(0, CORP_COUNT-1)),
        randint(0, 15))


csv_writer(
    'data/person_corp_share.csv',
    PERSON_SHAREHOLD_COUNT,
    person_share_generator)


# PERSON RELATION
def person_rel_generator():
    """
    (pid, pid, rel_degree)
    """
    return (
        'p_'+str(randint(0, PERSON_COUNT-1)),
        'p_'+str(randint(0, PERSON_COUNT-1)),
        randint(0, 99))


csv_writer(
    'data/person_rel.csv',
    PERSON_REL_COUNT,
    person_rel_generator)


# CORP RELATION
def corp_rel_generator():
    """
    (cid, cid)
    """
    return (
        'c_'+str(randint(0, CORP_COUNT-1)),
        'c_'+str(randint(0, CORP_COUNT-1)))


csv_writer(
    'data/corp_rel.csv',
    CORP_REL_COUNT,
    corp_rel_generator)


# CORP Shareholding
def corp_share_generator():
    """
    (cid, cid, share)
    """
    return (
        'c_'+str(randint(0, CORP_COUNT-1)),
        'c_'+str(randint(0, CORP_COUNT-1)),
        randint(0, 15))


csv_writer(
    'data/corp_share.csv',
    CORP_SHAREHOLD_COUNT,
    corp_share_generator)


# Person Corp Role
def person_corp_role_generator():
    """
    (pid, cid, role)
    """
    return (
        'p_'+str(randint(0, PERSON_COUNT-1)),
        'c_'+str(randint(0, CORP_COUNT-1)),
        faker.job())


csv_writer(
    'data/person_corp_role.csv',
    PERSON_ROLE_COUNT,
    person_corp_role_generator)

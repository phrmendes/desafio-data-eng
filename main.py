from pipelines.terceirizados.data import get_data

if __name__ == "__main__":
    result = get_data.serve(
        name="desafio_data_eng",
        cron="0 12 15 3,5,9 *",
        description="""
        Processing the data of subcontracted public administration workers.
        This task is carried out at 12:00 on the 15th of the month in March,
        May and September.
        """,
    )

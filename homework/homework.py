"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel



def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    import os
    import zipfile
    import pandas as pd

    client_df = pd.DataFrame(columns=[
        'client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage'
    ])

    campaign_df = pd.DataFrame(columns=[
        'client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts',
        'previous_outcome', 'campaign_outcome', 'last_contact_date'
    ])

    economics_df = pd.DataFrame(columns=[
        'client_id', 'cons_price_idx', 'euribor_three_months'
    ])

    # Descomprimir archivos
    for file in os.listdir("files/input"):
        if file.endswith(".zip"):
            with zipfile.ZipFile(f"files/input/{file}", "r") as zip_ref:
                for filename in zip_ref.namelist():  # Iterar sobre archivos dentro del ZIP
                    with zip_ref.open(filename) as f:  # Abrir archivo sin escribir en disco
                        df = pd.read_csv(f, sep=",")
# ,client_id,age,job,marital,education,credit_default,mortgage,month,day,contact_duration,number_contacts,
# previous_campaign_contacts,previous_outcome,cons_price_idx,euribor_three_months,campaign_outcome
                        df["job"] = df["job"].str.replace(".", "").str.replace("-", "_")
                        df["education"] = df["education"].str.replace(".", "_").replace("unknown", pd.NA)
                        df["credit_default"] = df["credit_default"].apply(lambda x: 1 if x == "yes" else 0)
                        df["mortgage"] = df["mortgage"].apply(lambda x: 1 if x == "yes" else 0)
                        client_df = pd.concat([client_df, df[["client_id", "age", "job", "marital", "education", 
                                                            "credit_default", "mortgage"]]])
                        
                        df["previous_outcome"] = df["previous_outcome"].apply(lambda x: 1 if x == "success" else 0)
                        df["campaign_outcome"] = df["campaign_outcome"].replace("yes", 1).replace("no", 0)
                        df["last_contact_date"] = pd.to_datetime("2022-" + df["month"] + "-" + df["day"].astype(str), format="%Y-%b-%d")
                        campaign_df = pd.concat([campaign_df, df[["client_id", "number_contacts", "contact_duration", 
                                                                "previous_outcome", "campaign_outcome", "last_contact_date"]]])

                        economics_df = pd.concat([economics_df, df[["client_id"]]])

                    
    client_df.to_csv("files/output/client.csv", index=False)
    campaign_df.to_csv("files/output/campaign.csv", index=False)
    economics_df.to_csv("files/output/economics.csv", index=False)               

    return


if __name__ == "__main__":
    clean_campaign_data()

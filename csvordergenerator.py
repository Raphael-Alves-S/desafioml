import requests
import json
import csv

def read_file(file):
    try:
        open_file = open(file, 'r')
        read_orders = open_file.read().split()
        if len(read_orders) == 0:
            return None
        else:
            return read_orders
    except FileNotFoundError as e:
        return (f"Arquivo não encontrado \n"
              f"{e}")

def entityorder(order):
    if order is not None:
        # Criacao do arquivo csv e escrita do cabecalho
        filecsv = open('csvimport.csv', 'w', newline='')
        fieldnames = "ID Ordem", "ID Item", "Descrição do produto", "ID Envio", "Estado", "Subestado", "Tipo de logistica", "Destino do envio", "ID Agência", "ID Carrier", "Endereço do Receptor"
        wrt = csv.writer(filecsv, delimiter=',')
        wrt.writerow(fieldnames)
        separator = ' '

        # Inicio entity orders
        for i in range(len(order)):
            requestorders = requests.get(
                'https://6f008c57-99e0-4a2e-8d80-782a71cf99db.mock.pstmn.io/orders/' + str(order[i]))
            orders = json.loads(requestorders.content)
            try:
                idorder = str(orders['id'])
                shipmentid = str(orders['shipping']['id'])

                for orderitems in orders['order_items']:
                    iditem = orderitems['item']['id']
                    nomeitem = orderitems['item']['title']
                    if orderitems['item']['variation_attributes'] is not None:
                        for attributes in orderitems['item']['variation_attributes']:
                            coratt = attributes['name'] + " " + attributes['value_name']
                    else:
                        coratt = ""

                # Inicio entity shipment
                requestshipment = requests.get(
                    'https://6f008c57-99e0-4a2e-8d80-782a71cf99db.mock.pstmn.io/shipments/' + str(shipmentid))
                shipments = json.loads(requestshipment.content)
                status = shipments['status']
                substatus = shipments['substatus']
                logistictype = shipments['logistic_type']
                receiver = shipments['receiver_address']['street_name'], shipments['receiver_address']['street_number'], \
                    shipments['receiver_address']['city']['name'], shipments['receiver_address']['zip_code']

                if shipments['receiver_address']['agency'] is not None:
                    recipient = "Agência"
                    agencyid = shipments['receiver_address']['agency']['agency_id']
                    carrierid = shipments['receiver_address']['agency']['carrier_id']
                else:
                    recipient = "Domicilio"
                    agencyid = ""
                    carrierid = ""

                # Escrita no CSV
                csvouput = idorder, iditem, nomeitem + ", " + coratt, shipmentid, status, substatus, logistictype, recipient, agencyid, carrierid, separator.join(
                    receiver)
                wrt.writerow(csvouput)
            except KeyError as e:
                return(f"Não foi possivel retornar informações para o dado "f"{order[i]}"" pois o parametro "f"{e} não "
                      f"existe \n"
                      f"{orders}")

        # Fechar arquivo
        filecsv.close()
        return "Sucesso"

    else:
        return "CSV não gerado, pois os dados estão vazios"


# chamada da funcao
entityorder(read_file('teste.txt'))


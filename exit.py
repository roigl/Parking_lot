import boto3
from datetime import datetime
import math


def get_item(ticket_id):

    client = boto3.client('dynamodb', region_name='us-east-1')

    item = client.scan(TableName = 'parking_logs',
                       FilterExpression = "ticket_id =:ticket_id",
                        ExpressionAttributeValues = {":ticket_id" : {"S":ticket_id}}
                        )
    return(item['Items'])

def delete_item(ticket_id,parking_lot_id):

    client = boto3.client('dynamodb', region_name='us-east-1')

    client.delete_item(
                       Key = { "parking_lot_id" : {"S" : parking_lot_id},
                                "ticket_id" : {"S": ticket_id }

                               },
                       TableName = 'parking_logs',
                        )


def exit(ticket_id):

    item = get_item(ticket_id)
    if len(item) > 0:
        item = item[0]
        now = datetime.now()
        entry_time = datetime.strptime(item['entry_time']['S'], '%m/%d/%y %H:%M:%S')
        total_time = (now - entry_time)
        total_time_15_min = int(math.ceil((total_time.seconds / 60) / 15))

        result = {'plate' : item['plate_id']['S'] ,
                'total parking time' : str(total_time),
                'parking lot id' :  item['parking_lot_id']['S'],
                'charge' : str(total_time_15_min*10)+'$'
                }

        delete_item(ticket_id,item['parking_lot_id']['S'])

        return result

    else:
        return "ticket number not recognized"

if __name__ == "__main__":
    print(exit("4"))

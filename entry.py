import boto3
from datetime import datetime


def ticket_id_generator():
    now = datetime.now()
    current_time = now.strftime("%d%m%y%H%M%S")

    return current_time

def check_if_exist(plate_id,parking_lot_id):

    client = boto3.client('dynamodb', region_name='us-east-1')

    item = client.scan(TableName='parking_logs',
                       FilterExpression= "plate_id =:plate_id",
                        ExpressionAttributeValues =   {":plate_id" : {"S":plate_id} }
                        )
    return len(item['Items'])



def entry(plate_id, parking_lot_id):

    if check_if_exist(plate_id, parking_lot_id) == 0:

        client = boto3.client('dynamodb', region_name='us-east-1')

        new_id = ticket_id_generator()

        now = datetime.now()
        current_time = now.strftime("%D %H:%M:%S")
        client.put_item(
            TableName='parking_logs',
            Item={
                'ticket_id': {'S': new_id },

                'plate_id': {'S': plate_id},
                'parking_lot_id': {'S': parking_lot_id},
                'entry_time': {'S': current_time}
            }
        )

        return new_id
    else:
        return "Car Plate Already in parking lot"

if __name__ == "__main__":
    print(entry("1456","0"))

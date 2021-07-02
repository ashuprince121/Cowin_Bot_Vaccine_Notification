import time
import requests
import schedule

from datetime import datetime

base_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now = datetime.now()
today_date = now.strftime("%d-%m-%Y")

#telegram api url
tg_api_url="https://api.telegram.org/bot1784237012:AAEHwx5k27NhnJ1n1QWNlE7mTYkKEFfbaFg/sendMessage?chat_id=@nowvaccine&text="


punjab_dist_ids=[479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495,496,497,498,499,500]

def fetch_data(district_id):  # fetch data from CoWin
    query_params = "?district_id={}&date={}".format(district_id, today_date)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    final_url = base_url + query_params
    response = requests.get(final_url, headers=headers)
    filter_avl_data(response)
    # print(response.text)

def fetch_for_states(district_ids):
    for i in district_ids:
        fetch_data(i)


def filter_avl_data(response):
    json_response=response.json()
    counter=0;

    for center in json_response["centers"]:
        message=""
        counter = counter+1
        if (counter>5):  #for running it only 5 times.
            break
        for session in center['sessions']:
            if(session['available_capacity_dose1']>0 and session['min_age_limit']==18):
                message+="Pincode:{}, \nName:{}, \nSlots: {},\nDate: {},\nVaccine: {},\nFee:{}, \nMinimum Age: {}\n-------\n".format(
                center["pincode"], center["name"],
                session["available_capacity_dose1"],
                session["date"], session["vaccine"], center["fee_type"],
                session["min_age_limit"]
                )
        send_txt_telegram(message)

def send_txt_telegram(message):
    tg_final_url = tg_api_url+message
    response = requests.get(tg_final_url)
    print(response)


if __name__=="__main__":
    schedule.every(10).seconds.do(lambda :(fetch_for_states(punjab_dist_ids)))
    while True:
        schedule.run_pending()
        time.sleep(1)



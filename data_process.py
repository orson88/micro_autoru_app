import pickle
import pandas as pd
from data_scrape import scrape_data

def main_processor():
    try:
        data = pd.read_pickle('autoru_proj_data.pkl')
    except:
        scrape_data()
        data = pd.read_pickle('autoru_proj_data.pkl')
    data = pd.read_pickle('autoru_proj_data.pkl')
    df = pd.DataFrame(data, columns=['saleId', 'section', 'seller_type', 'price_info', 'documents', 'seller', 'state', 'vehicle_info'])
    print(df.head(5))
    df['price'] = 0
    print('read')
    currencies = []
    prices = []
    for r in range(len(df)):
        prices.append(df['price_info'][r]['price'])
        currencies.append(df['price_info'][r]['currency'])
    df['price'] = prices
    df['currency'] = currencies
    df.drop(columns=['currency', 'price_info'], inplace=True)
    print('currency')
    years = []
    owners = []
    for r in range(len(df)):
        years.append(df['documents'][r]['year'])
        if 'owners_number' in list(df['documents'][r].keys()):
            owners.append(df['documents'][r]['owners_number'])
        else:
            owners.append(None)
    df['year'] = years
    df['owners'] = owners
    df.drop('documents', axis=1, inplace=True)
    print('documents')
    images = []
    mileages = []
    latitudes = []
    longitudes = []
    city_names = []
    for r in range(len(df)):
        images.append(df['state'][r]['images_count'])
        mileages.append(df['state'][r]['mileage'])
        latitudes.append(df['seller'][r]['location']['coord']['latitude'])
        longitudes.append(df['seller'][r]['location']['coord']['longitude'])
        city_names.append(df['seller'][r]['location']['region_info']['name'])
    df['images'] = images
    df['milage'] = mileages
    df['latitude'] = latitudes
    df['longitude'] = longitudes
    df['city_name'] = city_names
    df.drop(columns=['state', 'seller'], inplace=True)
    print('location')
    model_names = []
    steering_wheels = []
    body_types = []
    engine_types = []
    transmissions = []
    gear_types = []
    horsepowers = []
    fuel_rates = []
    doors = []
    trunk_volumes = []
    for r in range(len(df)):
        model_names.append(df['vehicle_info'][r]['model_info']['code'])
        steering_wheels.append(df['vehicle_info'][r]['steering_wheel'])
        body_types.append(df['vehicle_info'][r]['configuration']['body_type'])
        engine_types.append(df['vehicle_info'][r]['tech_param']['engine_type'])
        transmissions.append(df['vehicle_info'][r]['tech_param']['transmission'])
        gear_types.append(df['vehicle_info'][r]['tech_param']['gear_type'])
        horsepowers.append(df['vehicle_info'][r]['tech_param']['power'])
        if 'fuel_rate' in list(df['vehicle_info'][r]['tech_param'].keys()):
            fuel_rates.append(df['vehicle_info'][r]['tech_param']['fuel_rate'])
        else:
            fuel_rates.append(None)
        if 'trunk_volume_min' in list(df['vehicle_info'][r]['configuration'].keys()):
            trunk_volumes.append(df['vehicle_info'][r]['configuration']['trunk_volume_min'])
        else:
            trunk_volumes.append(None)
        doors.append(df['vehicle_info'][r]['configuration']['doors_count'])
    df['model_name'] = model_names
    df['steering_wheel'] = steering_wheels
    df['body_type'] = body_types
    df['engine_type'] = engine_types
    df['transmission'] = transmissions
    df['gear_type'] = gear_types
    df['horsepower'] = horsepowers
    df['fuel_rate'] = fuel_rates
    df['doors'] = doors
    df['trunk_volume'] = trunk_volumes
    print('techs')
    equipment_list = []
    for r in range(len(df)):
        for elem in list(df['vehicle_info'][r]['equipment'].keys()):
            if elem not in equipment_list:
                equipment_list.append(elem)
    equipment = []
    for r in range(len(df)):
        equipment.append(list(df['vehicle_info'][r]['equipment'].keys()))
    df['equipment'] = equipment
    df.drop('vehicle_info', axis=1, inplace=True)
    df.loc[:, equipment_list] = 0
    for i in range(len(df)):
        for j in range(len(df.columns)):
            if df.iloc[:, j].name in df['equipment'][i]:
                df.iloc[i, j] = 1
    df.drop('equipment', axis=1, inplace=True)
    print('done')
    df.to_csv('auto_data.csv', index = False)
    print('saved')

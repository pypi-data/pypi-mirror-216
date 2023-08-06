import json

cites_json = 'meta_data/top_cites.json'
health_tour_spot = 'meta_data/health_tourism.json'


class CitesApi:
    def __init__(self):
        with open(cites_json, 'rb') as fb:
            self.cites_data = json.load(fb)

    def get_top_cites_names(self):
        top_cites = self.cites_data.get('top_cites').keys()
        return top_cites

    def get_cites_images(self, cite):
        images_cid = self.cites_data['top_cites'][cite]['images']
        images_link = []
        for cid in images_cid:
            images_link.append(f'https://nftstorage.link/ipfs/{cid}')
        return images_link

    def get_cite_summary(self, cite):
        summary = self.cites_data['top_cites'][cite]['summary']
        return summary

    def get_cite_coordinates(self, cite):
        coordinates = self.cites_data['top_cites'][cite]['coordinates']
        return coordinates

    def get_major_health_institutes(self):
        return self.cites_data['top_health_institutes']

    def get_tourist_spots(self):
        return self.cites_data['top_tourist_spots']

    def get_low_cost_medical_procedures(self):
        return self.cites_data['low_cost_medical_procedures']


class HospitalsApis:
    def __init__(self, type):
        json_path = f'{type}_hospital.json'
        with open(json_path, 'r') as fb:
            self.hsptl_data = json.load(fb)

    def get_hospital_list(self):
        name_list = []
        for i in self.hsptl_data:
            name_list.append(i['Name of medical facility'])
        print(len(name_list))
        return name_list

    def get_hospital_image(self, name):
        images_link = []
        for i in self.hsptl_data:
            if i['Name of medical facility'] == name:
                for cid in i['images']:
                    images_link.append(f'https://nftstorage.link/ipfs/{cid}')
        return images_link

    def get_hospital_url(self, name):
        for i in self.hsptl_data:
            if i['Name of medical facility'] == name:
                return i["website"]


class HealthTourismApis:
    def __init__(self):
        with open(health_tour_spot, 'rb') as fb:
            self.health_tour_data = json.load(fb)

    def get_health_tour_spots(self):
        tour_spots = self.health_tour_data.keys()
        return tour_spots

    def get_spot_summary(self, spot_name):
        return self.health_tour_data[spot_name]['summary']

    def get_spot_coordinates(self, spot_name):
        return self.health_tour_data[spot_name]['coordinates']

    def get_spot_images(self, spot_name):
        images_cid = self.health_tour_data[spot_name]['images']
        images_link = []
        for cid in images_cid:
            images_link.append(f'https://nftstorage.link/ipfs/{cid}')
        return images_link

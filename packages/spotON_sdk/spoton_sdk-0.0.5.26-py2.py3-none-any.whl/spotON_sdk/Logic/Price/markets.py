from .spotON_Areas import spotON_Area,Area_details
import pandas as pd
from dataclasses import dataclass, field
from typing import Optional, Dict,Any

from typing import List
from .countries import *
from .bidding_zones import bidding_zones

from .customBaseModel import CustomBaseModel

from pydantic import Field, root_validator,validate_model

class Market(CustomBaseModel):
    area: Area_details
    country: Country
    alias: Optional[str] = None
    cities: str = Field(default="")
    name: str = Field(default="")
    @root_validator(pre=True)
    def set_codes(cls, values):
        country = values.get('country')
        if country and 'country_name' in country:
            values["name"] = country['country_name']
        return values

    '''@root_validator(pre=True)
    def set_codes(cls, values):
        area = values.get('area')
        print(type(area))
        area_code = area.name
        print(type(area_code))
        values['area_code'] = area_code

        country_region = area_code.split("_")
        values['country_code'] = country_region[0]
        if len(country_region) >=2:
            values['region_code'] = country_region[1]

        try:
            city_List = bidding_zones[area_code]["cities"]
            my_string = ', '.join(city_List)
            values['cities'] = my_string
        except:
            values['cities'] = ""

        values["name"] = f"{values['country'].country_name} {values['area_code']} {values['cities']}"
        return values


        #TODO: Add emoji to name
        self.name = f"{self.country.country_name} {self.area_code} {self.cities}"
        self.name = f" {self.country.country_name}"

        self.name = f"{self.country.emoji} {self.country.country_name} {self.area_code} {self.cities}"
        self.name = f"{self.country.emoji} {self.country.country_name}"'''

        #self.get_Market_by_area_code(self.area.name)






class Markets():

    austria = Market(area=spotON_Area.AT.value,country=all_Countries.Austria)
    germany = Market(area=spotON_Area.DE_LU.value,country=all_Countries.Germany,alias="DE_LU")
    sweden1 = Market(area=spotON_Area.SE_1.value,country=all_Countries.Sweden)    
    #luxembourg = Market(Area.DE_LU,Luxembourg)

    #sweden2 = Market(Area.SE_2,Sweden)
    #sweden3 = Market(Area.SE_3,Sweden)
    #sweden4 = Market(Area.SE_4,Sweden)
    markets_List = [value for key, value in vars().items() if isinstance(value, Market)]
    merged_Markets = []

    @staticmethod
    def get_market_by_name(name: str) -> Optional[Market]:
        for market in Markets.markets_List:
            if market.name == name: # type: ignore
                return market

        return None

    @staticmethod
    def get_market_by_code(area_code: str) -> Optional[Market]:
        for market in Markets.markets_List:
            #print (f"Try to find {area_code =} in {market}")
            if market.country_code == area_code or market.alias == area_code:
                return market

        return None






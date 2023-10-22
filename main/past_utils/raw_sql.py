def raw_sql_search_result_address(query):
    return """SELECT DISTINCT main_propertyimages.property_id as id, 
        images, price, title, 
        address, neighborhood, area, city, state, postcode, latitude, longitude,
        bedrooms, bathrooms, square_footage, property_type,
        price_unit, bedrooms_unit
        FROM main_property
        LEFT JOIN main_propertyimages on main_property.id = main_propertyimages.property_id
        LEFT JOIN main_propertyinfo on main_propertyimages.property_id = main_propertyinfo.property_id
        LEFT JOIN main_propertyaddress on main_propertyinfo.property_id = main_propertyaddress.property_id
        LEFT JOIN main_propertyaddunit on main_propertyaddress.property_id = main_propertyaddunit.property_id
        LEFT JOIN main_propertyamenities on main_propertyaddunit.property_id = main_propertyamenities.property_id

        WHERE  address == %(address)s AND city = %(city)s
         AND state = %(state)s AND postcode = %(postcode)s
        GROUP by 1
        ORDER by time_update desc""", query


def raw_sql_search_result_neighborhood_area(query):
    return """SELECT DISTINCT main_propertyimages.property_id as id, 
        images, price, title, 
        address, neighborhood, area, city, state, postcode, latitude, longitude,
        bedrooms, bathrooms, square_footage, property_type,
        price_unit, bedrooms_unit
        FROM main_property
        LEFT JOIN main_propertyimages on main_property.id = main_propertyimages.property_id
        LEFT JOIN main_propertyinfo on main_propertyimages.property_id = main_propertyinfo.property_id
        LEFT JOIN main_propertyaddress on main_propertyinfo.property_id = main_propertyaddress.property_id
        LEFT JOIN main_propertyaddunit on main_propertyaddress.property_id = main_propertyaddunit.property_id
        LEFT JOIN main_propertyamenities on main_propertyaddunit.property_id = main_propertyamenities.property_id

        WHERE  (neighborhood == %(neighborhood_area)s or area == %(neighborhood_area)s) 
         AND city = %(city)s AND state = %(state)s
        GROUP by 1
        ORDER by time_update desc""", query


def raw_sql_search_result_city(query):
    return """SELECT DISTINCT main_propertyimages.property_id as id,
        images, price, title,
        address, neighborhood, area, city, state, postcode, latitude, longitude,
        bedrooms, bathrooms, square_footage, property_type,
        price_unit, bedrooms_unit
        FROM main_property
        LEFT JOIN main_propertyimages on main_property.id = main_propertyimages.property_id
        LEFT JOIN main_propertyinfo on main_propertyimages.property_id = main_propertyinfo.property_id
        LEFT JOIN main_propertyaddress on main_propertyinfo.property_id = main_propertyaddress.property_id
        LEFT JOIN main_propertyaddunit on main_propertyaddress.property_id = main_propertyaddunit.property_id
        LEFT JOIN main_propertyamenities on main_propertyaddunit.property_id = main_propertyamenities.property_id

        WHERE  city = %(city)s AND state = %(state)s
        GROUP by 1
        ORDER by time_update desc""", query


def raw_sql_search_result_postcode(query):
    return """SELECT DISTINCT main_propertyimages.property_id as id,
        images, price, title,
        address, neighborhood, area, city, state, postcode, latitude, longitude,
        bedrooms, bathrooms, square_footage, property_type,
        price_unit, bedrooms_unit
        FROM main_property
        LEFT JOIN main_propertyimages on main_property.id = main_propertyimages.property_id
        LEFT JOIN main_propertyinfo on main_propertyimages.property_id = main_propertyinfo.property_id
        LEFT JOIN main_propertyaddress on main_propertyinfo.property_id = main_propertyaddress.property_id
        LEFT JOIN main_propertyaddunit on main_propertyaddress.property_id = main_propertyaddunit.property_id
        LEFT JOIN main_propertyamenities on main_propertyaddunit.property_id = main_propertyamenities.property_id

        WHERE  postcode = %(postcode)s
        GROUP by 1
        ORDER by time_update desc""", query
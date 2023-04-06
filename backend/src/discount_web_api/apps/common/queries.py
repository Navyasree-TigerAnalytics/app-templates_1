from core.generics.exceptions import MissingRequestParamsError


def fixedPromos():

    querystring = "select fo.fixed_offer_id,vfo.coop,vfo.promo_type,vfo.coop_ohm_id,vfo.pt_ohm_id,vfo.channel,vfo.start_date,vfo.duration,vfo.dis_mech_id,vfo.dis_mech_desc,\
    vfo.item_grp_id,vfo.item_grp_desc,vfo.offer_desc,vfo.offer_daypart,vfo.is_lto,vfo.base_price,vfo.promo_price,vfo.discount_depth_per,fo.created_by,fo.modified_at\
    from public.fixed_offers fo INNER Join vw_fixed_offers vfo on fo.ohm_id = vfo.pt_ohm_id\
    where vfo.coop=%s and vfo.start_date=%s and vfo.duration=%s;"

    return querystring


def usergoes(user_id):
    query_string = f"""
    SELECT a.ohm_id, a.ohm_desc AS coop_name, a.ohm_code 
        FROM offer_hier_master a 
        JOIN user_geo_mapping b ON b.hierarchy_code = a.ohm_code 
        WHERE 
        b.user_id = {user_id};
    """
    return query_string

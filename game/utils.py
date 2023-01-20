import folium

from .models import GameResult

def create_map(game, user, play):
    if play:
        result = GameResult.objects.filter(player=user).get(game=game)
        caches = game.game_cache.filter(order__lte=result.found_caches+1)
    else:
        result = GameResult.objects.filter(game=game).order_by('found_caches').first()
        caches = game.game_cache.all()

    start_coords = (game.latitude, game.longitude)
    folium_map = folium.Map(location=start_coords, zoom_start=game.zoom, attr="https://www.openstreetmap.org/#map=6/40.007/-2.488")

    for cache in caches:
        popup = ''
        if cache.hint_picture:
            hint = ''
            if cache.hint_picture:
                hint = '<div style="display:flex;width:100%;font-weight:bold;min-width: 100px;"><p style="color:red">' + str(cache.order) + ') </p><p style="text-align:center;width:100%;">' + cache.hint + '<span></span></p></div>'
            
            popup = '<div>' + hint + '<img src="' + cache.hint_picture.url +'" style="max-width:150px;"/></div>'
        else:
            popup = '<div style="display:flex;width:100%;font-weight:bold;min-width: 100px;"><p style="color:red">' + str(cache.order) + ') </p><p style="text-align:center;width:100%;">' + cache.hint + '<span></span></p></div>'
        
        coords = (cache.latitude, cache.longitude)


        if cache.order != result.found_caches+1:
            folium.Marker(location=coords, popup=popup, icon=folium.Icon(color="green", icon="check")).add_to(folium_map)
        else:
            folium.Marker(location=coords, popup=popup, icon=folium.Icon(color="blue", icon="zoom-in")).add_to(folium_map)

    folium_map = folium_map._repr_html_()
    return folium_map
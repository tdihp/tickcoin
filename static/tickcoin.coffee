window.tickcoin = {}

ENDPOINT_PREFIX = ''

tickcoin.slots = []  # [{name, current_counter, ticks, available_counters: [{counter_name, text, active}]}]
slot_template = Handlebars.templates.slot  # compile($("#tickcoin_slot_template").html())

on_error = (err_msg) ->
    alert(err_msg)

get_ticks = (slot_name, counter_name, callback) ->
    url = "#{ENDPOINT_PREFIX}/slots/#{slot_name}/counters/#{counter_name}"
    $.get(url, (data, textStatus, jqXHR) ->
        result = data  # JSON.parse(data)
        callback(result.ticks)
    ).fail((jqXHR, textStatus, errorThrown) ->
        on_error("failed to get ticks of #{url} because #{errorThrown}")
    )


tick_slot = (slot_name, callback) ->
    url = "#{ENDPOINT_PREFIX}/slots/#{slot_name}/ticks"  # this endpoint is only for posting ticks for now

    # csrf token
    csrftoken = $.cookie('csrftoken')

    $.ajax({
        type: 'POST',
        url: url,
        beforeSend: ((req) ->
            if csrftoken?
                req.setRequestHeader('X-CSRFToken', csrftoken)
        ),
        success: (data, textStatus, jqXHR) ->
            result = data  # JSON.parse(data)
            # not really useful, for now
            callback()
    }).fail((jqXHR, textStatus, errorThrown) ->
        on_error("failed to tick #{url} because #{errorThrown}")
    )


get_slots = (callback) ->
    url = "#{ENDPOINT_PREFIX}/slots"
    $.get(url, (data, textStatus, jqXHR) ->
        result = data  #JSON.parse(data)
        callback(result.slots)
    ).fail((jqXHR, textStatus, errorThrown) ->
        on_error("failed to get slots #{url} because #{errorThrown}")
    )


# update slot data structure for rendering
refresh_slot = (slot, ticks, counter_name) ->
    slot.current_counter = counter_name
    slot.ticks = ticks
    if not counter_name?
        # XXX: always have available counters
        counter_name = slot.available_counters[0].counter_name
        slot.current_counter = counter_name

    for counter in slot.available_counters
        if counter_name == counter.counter_name
            counter.active = true
        else
            counter.active = false


render_all = () ->
    $('#tickcoin_slots').empty()
    for slot in tickcoin.slots
        do (slot) ->
            $('#tickcoin_slots').append(slot_template(slot))
            slot_callback(slot)


all = (arr, func, callback)->
    for v in arr
        if not func(v)
            return false
    callback()
    return true


disable_clicks = (slot_selector) ->
    $("#{slot_selector} > .ticker").removeAttr('href')
    $("#{slot_selector} > .counter-switcher").removeAttr('href')


slot_callback = (slot)->
    slot_id = "#slot-#{slot.name}"

    # tick callback
    $("#{slot_id} > .ticker").click((event)->
        # disable the click
        disable_clicks(slot_id)
        # send tick
        tick_slot(slot.name, ()->
            # get ticks again
            get_ticks(slot.name, slot.current_counter, (ticks) ->
                # refresh view
                slot.ticks = ticks
                $(slot_template(slot)).replaceAll(slot_id)
                slot_callback(slot)
            )
        )
    )

    # switch callback
    $("#{slot_id} > .counter-switcher").click((event)->
        # disable all switcher clicks
        disable_clicks(slot_id)
        counter_name = event.target['counter-name']
        get_ticks(slot.name, counter_name, (ticks)->
            refresh_slot(slot, ticks, counter_name)
            $(slot_id).replaceAll(slot_template(slot))
            slot_callback(slot)
        )
    )


$(document).ready(
    get_slots((slots) ->
        tickcoin.slots = slots
        for slot in slots
            do (slot) ->
                refresh_slot(slot)
                get_ticks(slot.name, slot.current_counter, (ticks)->
                    refresh_slot(slot, ticks, slot.current_counter)
                    all(tickcoin.slots, ((slot) -> slot.ticks?), () ->
                        render_all()
                    )
                )
    )
)

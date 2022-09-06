from re import L
TOTAL_LEDS = 9
LED_BRIGHTNESS_MAX = 127
TC_LIGHT_MAPPING = {
    0: 57,
    1: 58,
    2: 59,
    3: 60,
    4: 61,
    5: 62,
    6: 63,
    7: 64,
    8: 65
}

def generate_led(volume):
    # Filter out bad input for volume. Volume show be between 0 and 1
    volume = float(volume) if volume != None else float(0)
    led_unit_value = float( round( ( float(1) / float(TOTAL_LEDS // 2) ) , 4) )
    full_led_number = int( volume // led_unit_value )
    partial_led_unit_value = round( volume % led_unit_value, 4 )
    led_cc_values = []
    middle_led = TOTAL_LEDS // 2 + TOTAL_LEDS % 2
    for led in range(TOTAL_LEDS):
        if volume < 0:
            pass
        elif volume > 0:
            pass
        else:
            pass
        if led < full_led_number:
            led_cc_values.append( (led, 127) )
        if led == full_led_number:
            cc_value = round( 127 * (partial_led_unit_value / led_unit_value) )
            led_cc_values.append( (led, cc_value) )
        if led > full_led_number:
            led_cc_values.append(( led, 0) )
    return led_cc_values
def generate_pan_meter_led_values(segments, volume):
    is_positive = False if volume < 0 else True
    half = (segments // 2 )
    has_middle = True if segments % 2 != 0 else False
    full_led = abs( int( float(volume) // ( float(1) / float(half) ) ) )
    partial_led = int( round( 127 *  ( float(volume) % ( float(1) / float(half) ) ) ) )  
    vector = 1 if is_positive else -1
    shift = half
    if is_positive and has_middle:
        shift +1
    if not is_positive:
        shift -= 1
    leds = {}
    for x in range(full_led + 1):
        if x < (full_led):
            leds[x*vector + shift] = 127
        if partial_led != 0 :
            leds[x*vector + shift]=  partial_led
    print(leds)
    meter_values = []
    for y in range(segments):
        if y in leds:
            meter_values.append((y, leds[y]))
        else:
            if y == half and has_middle:
                meter_values.append((y, 127))
            else:
                meter_values.append((y, 0))
    return meter_values
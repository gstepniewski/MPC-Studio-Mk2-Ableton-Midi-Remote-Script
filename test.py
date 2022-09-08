import os
REPEAT_LIGHT_MAPPING = {
    0: 110,
    1: 109,
    2: 108,
    3: 107,
    4: 106,
    5: 105,
    6: 104,
    7: 103
}
def generate_repeat_display_values(value):
    value = int(value) if value != '' else None
    light_unselected = 8
    light_selected = 127
    light_off = 0
    selected_index = value // 16 if value else None
    light_cc_mapping = []
    for light in REPEAT_LIGHT_MAPPING:
        if value:
            cc_value = light_selected if light == selected_index else light_unselected
            light_cc_mapping.append((light, cc_value))
        else:
            light_cc_mapping.append((light, light_off))
    return light_cc_mapping

input1 = input()
while input1 != 'exit':
    section(input1)
    input1 = input()
    os.system('cls')
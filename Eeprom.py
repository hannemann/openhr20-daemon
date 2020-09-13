def get_eeprom_layout(layout_id, hr25=False):
    layout = [
        {
            'idx': '00',
            'name': 'lcd_contrast',
            'description': '',
            'type': 'int',
            'range': [1, 15]
        },
        {
            'idx': '01',
            'name': 'temperature0',
            'description': 'temperature 0  - frost protection (unit is 0.5stC)',
            'type': 'int',
            'range': [10, 60]
        },
        {
            'idx': '02',
            'name': 'temperature1',
            'description': 'temperature 1  - energy save (unit is 0.5stC)',
            'type': 'int',
            'range': [10, 60]
        },
        {
            'idx': '03',
            'name': 'temperature2',
            'description': 'temperature 2  - comfort (unit is 0.5stC)',
            'type': 'int',
            'range': [10, 60]
        },
        {
            'idx': '04',
            'name': 'temperature3',
            'description': 'temperature 3  - supercomfort (unit is 0.5stC)',
            'type': 'int',
            'range': [10, 60]
        },
        {
            'idx': '05',
            'name': 'P3_Factor',
            'description': 'Proportional kvadratic tuning constant, multiplied with 256',
            'range': [0, 255]
        },
        {
            'idx': '06',
            'name': 'P_Factor',
            'description': 'Proportional tuning constant, multiplied with 256',
            'type': 'int',
            'range': [0, 255]
        },
        {
            'idx': '07',
            'name': 'I_Factor',
            'description': 'Integral tuning constant, multiplied with 256',
            'type': 'int',
            'range': [0, 255]
        },
        {
            'idx': '08',
            'name': 'I_max_credit',
            'description': 'credit for interator limitation',
            'type': 'int',
            'range': [0, 127]
        },
        {
            'idx': '09',
            'name': 'I_credit_expiration',
            'description': 'unit is PID_interval',
            'type': 'int',
            'range': [0, 255]
        },
        {
            'idx': '0a',
            'name': 'PID_interval',
            'description': 'PID_interval*5 = interval in seconds',
            'type': 'int',
            'range': [20 / 5, 255]
        },
        {
            'idx': '0b',
            'name': 'valve_min',
            'description': 'valve position limiter min',
            'type': 'percent',
            'range': [0, 100]
        },
        {
            'idx': '0c',
            'name': 'valve_center',
            'description': 'default valve position for "zero - error" - improve stabilization after change temperature',
            'type': 'percent',
            'range': [0, 100]
        },
        {
            'idx': '0d',
            'name': 'valve_max',
            'description': 'valve position limiter max',
            'type': 'percent',
            'range': [0, 100]
        },
        {
            'idx': '0e',
            'name': 'valve_hysteresis',
            'description': 'valve movement hysteresis (unit is 1/128%)',
            'type': 'int',
            'range': [0, 127]
        },
        {
            'idx': '0f',
            'name': 'motor_pwm_min',
            'description': 'min PWM for motor',
            'type': 'int',
            'range': [32, 255]
        },
        {
            'idx': '10',
            'name': 'motor_pwm_max',
            'description': 'max PWM for motor',
            'type': 'int',
            'range': [50, 255]
        },
        {
            'idx': '11',
            'name': 'motor_eye_low',
            'description': 'min signal lenght to accept low level (multiplied by 2)',
            'type': 'int',
            'range': [1, 255]
        },
        {
            'idx': '12',
            'name': 'motor_eye_high',
            'description': 'min signal lenght to accept high level (multiplied by 2)',
            'type': 'int',
            'range': [1, 255]
        },
        {
            'idx': '13',
            'name': 'motor_close_eye_timeout',
            'description': 'time from last pulse to disable eye [1/61sec]',
            'type': 'int',
            'range': [5, 255]
        },
        {
            'idx': '14',
            'name': 'motor_end_detect_cal',
            'description': 'stop timer threshold in % to previous average',
            'type': 'int',
            'range': [110, 255]
        },
        {
            'idx': '15',
            'name': 'motor_end_detect_run',
            'description': 'stop timer threshold in % to previous average',
            'type': 'int',
            'range': [110, 255]
        },
        {
            'idx': '16',
            'name': 'motor_speed',
            'description': '/8',
            'type': 'int',
            'range': [10, 255]
        },
        {
            'idx': '17',
            'name': 'motor_speed_ctl_gain',
            'description': '',
            'type': 'int',
            'range': [10, 200]
        },
        {
            'idx': '18',
            'name': 'motor_pwm_max_step',
            'description': '',
            'type': 'int',
            'range': [1, 54]
        },
        {
            'idx': '19',
            'name': 'MOTOR_ManuCalibration_L',
            'description': '',
            'type': 'int',
            'range': [0, 255]
        },
        {
            'idx': '1a',
            'name': 'MOTOR_ManuCalibration_H',
            'description': '',
            'type': 'int',
            'range': [0, 255]
        },
        {
            'idx': '1b',
            'name': 'temp_cal_table0',
            'description': 'temperature calibration table, value for 35C',
            'type': 'int',
            'range': [0, 255]
        },
        {
            'idx': '1c',
            'name': 'temp_cal_table1',
            'description': 'temperature calibration table, value for 30C',
            'type': 'int',
            'range': [16, 255]
        },
        {
            'idx': '1d',
            'name': 'temp_cal_table2',
            'description': 'temperature calibration table, value for 25C',
            'type': 'int',
            'range': [16, 255]
        },
        {
            'idx': '1e',
            'name': 'temp_cal_table3',
            'description': 'temperature calibration table, value for 20C',
            'type': 'int',
            'range': [16, 255]
        },
        {
            'idx': '1f',
            'name': 'temp_cal_table4',
            'description': 'temperature calibration table, value for 15C',
            'type': 'int',
            'range': [16, 255]
        },
        {
            'idx': '20',
            'name': 'temp_cal_table5',
            'description': 'temperature calibration table, value for 10C',
            'type': 'int',
            'range': [16, 255]
        },
        {
            'idx': '21',
            'name': 'temp_cal_table6',
            'description': 'temperature calibration table, value for 05C',
            'type': 'int',
            'range': [16, 255]
        },
        {
            'idx': '22',
            'name': 'timer_mode FIX!!',
            'description': '0: only one program, 1: programs for weekdays',
            'type': 'int',
            'range': [0, 1]
        }
    ]

    idx = 34

    if hr25 is True:
        idx += 1
        layout.append({
            'idx': hex(idx)[2:4],
            'name': 'bat_half_thld',
            'description': 'treshold for half battery warning [unit 0.02V]=[unit 0.01V per cell]',
            'type': 'int',
            'range': [80, 160]
        })
    idx += 1
    layout.append({
        'idx': hex(idx)[2:4],
        'name': 'bat_warning_thld',
        'description': 'treshold for battery warning [unit 0.02V]=[unit 0.01V per cell]',
        'type': 'int',
        'range': [80, 160]
    })
    idx += 1
    layout.append({
        'idx': hex(idx)[2:4],
        'name': 'bat_low_thld',
        'description': 'threshold for battery low [unit 0.02V]=[unit 0.01V per cell]',
        'type': 'int',
        'range': [80, 160]
    })
    idx += 1
    layout.append({
        'idx': hex(idx)[2:4],
        'name': 'allow_ADC_during_motor',
        'description': '',
        'type': 'boolean',
        'range': [0, 1]
    })

    if layout_id == 0x15:
        ''' HW Window Detection '''
        idx += 1
        layout.append({
            'idx': hex(idx)[2:4],
            'name': 'window_open_detection_enable',
            'description': '',
            'type': 'boolean',
            'range': [0, 1]
        })
        idx += 1
        layout.append({
            'idx': hex(idx)[2:4],
            'name': 'window_open_detection_delay',
            'description': '[sec] max 4 minutes',
            'type': 'int',
            'range': [0, 240]
        })
        idx += 1
        layout.append({
            'idx': hex(idx)[2:4],
            'name': 'window_close_detection_delay',
            'description': '[sec] max 4 minutes',
            'type': 'int',
            'range': [0, 240]
        })
    elif layout_id == 0x14:
        idx += 1
        layout.append({
            'idx': hex(idx)[2:4],
            'name': 'window_open_detection_diff',
            'description': 'threshold for window open/close detection unit is 0.01C',
            'type': 'int',
            'range': [7, 255]
        })
        idx += 1
        layout.append({
            'idx': hex(idx)[2:4],
            'name': 'window_close_detection_diff',
            'description': 'threshold for window open/close detection unit is 0.01C',
            'type': 'int',
            'range': [7, 255]
        })
        idx += 1
        layout.append({
            'idx': hex(idx)[2:4],
            'name': 'window_open_detection_time',
            'description': 'unit 15sec = 1/4min',
            'type': 'int',
            'range': [1, 255]
        })
        idx += 1
        layout.append({
            'idx': hex(idx)[2:4],
            'name': 'window_close_detection_time',
            'description': 'unit 15sec = 1/4min',
            'type': 'int',
            'range': [1, 255]
        })
        idx += 1
        layout.append({
            'idx': hex(idx)[2:4],
            'name': 'window_open_timeout',
            'description': 'maximum time for window open state [minutes]',
            'type': 'int',
            'range': [2, 255]
        })

    ''' PLACE BOOST_CONTROLER_AFTER_CHANGE CONFIGURATION HERE '''
    ''' PLACE TEMP_COMPENSATE_OPTION CONFIGURATION HERE '''

    idx += 1
    layout.append({
        'idx': hex(idx)[2:4],
        'name': 'RFM_devaddr',
        'description': 'HR20\'s own device address in RFM radio networking. =0 mean disable radio',
        'type': 'int',
        'range': [0, 29]
    })
    idx += 1
    layout.append({
        'idx': hex(idx)[2:4],
        'name': 'security_key0',
        'description': 'key for encrypted radio messages',
        'type': 'int',
        'range': [0, 255]
    })
    idx += 1
    layout.append({
        'idx': hex(idx)[2:4],
        'name': 'security_key1',
        'description': 'key for encrypted radio messages',
        'type': 'int',
        'range': [0, 255]
    })
    idx += 1
    layout.append({
        'idx': hex(idx)[2:4],
        'name': 'security_key2',
        'description': 'key for encrypted radio messages',
        'type': 'int',
        'range': [0, 255]
    })
    idx += 1
    layout.append({
        'idx': hex(idx)[2:4],
        'name': 'security_key3',
        'description': 'key for encrypted radio messages',
        'type': 'int',
        'range': [0, 255]
    })
    idx += 1
    layout.append({
        'idx': hex(idx)[2:4],
        'name': 'security_key4',
        'description': 'key for encrypted radio messages',
        'type': 'int',
        'range': [0, 255]
    })
    idx += 1
    layout.append({
        'idx': hex(idx)[2:4],
        'name': 'security_key5',
        'description': 'key for encrypted radio messages',
        'type': 'int',
        'range': [0, 255]
    })
    idx += 1
    layout.append({
        'idx': hex(idx)[2:4],
        'name': 'security_key6',
        'description': 'key for encrypted radio messages',
        'type': 'int',
        'range': [0, 255]
    })
    idx += 1
    layout.append({
        'idx': hex(idx)[2:4],
        'name': 'security_key7',
        'description': 'key for encrypted radio messages',
        'type': 'int',
        'range': [0, 255]
    })

    layout.append({
        'idx': 'ff',
        'name': 'LAYOUT_VERSION',
        'description': '',
        'range': [20, 21],
        'readonly': True
    })

    return layout

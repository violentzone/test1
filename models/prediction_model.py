import streamlit as st
from models.util import calculate_and_set, predict_plot, HrControl


# ==========
def prediction_view():
    st.subheader('存活曲線預測')
    # Set "pred_copy" related controls
    if "pred_copy" not in st.session_state:
        # If baseline and prediction all not input
        st.session_state['pred_copy'] = False

    # If copy from explanation is activated
    if st.session_state['pred_copy']:
        # blue copy if there's value in baseline model
        if 'risk_value_col1' in st.session_state:
            hr1 = st.session_state['risk_value_col1']
            st.session_state['risk_value_col1_pred'] = hr1
        # blue set to 1 if copy from baseline clicked but baseline not set
        else:
            hr1 = 1
            st.session_state['risk_value_col1_pred'] = hr1

        if 'risk_value_col2' in st.session_state:
            hr2 = st.session_state['risk_value_col2']
            st.session_state['risk_value_col2_pred'] = hr2
        else:
            hr2 = 1
            st.session_state['risk_value_col2_pred'] = hr2

    # If copy from explanation is not activated
    else:
        if 'risk_value_col1_pred' not in st.session_state:
            st.session_state['risk_value_col1_pred'] = HrControl.risk_calculation()
            hr1 = st.session_state['risk_value_col1_pred']

        else:
            hr1 = st.session_state['risk_value_col1_pred']

        if 'risk_value_col2_pred' not in st.session_state:
            st.session_state['risk_value_col2_pred'] = 1.0
            hr2 = st.session_state['risk_value_col2_pred']
        else:
            hr2 = st.session_state['risk_value_col2_pred']

    # Determine if showblue or showred button is clicked
    if 'showblue' not in st.session_state:
        st.session_state['showblue'] = False
    if 'showred' not in st.session_state:
        st.session_state['showred'] = False

    # plotting
    with st.container():
        col1, col2 = st.columns([1, 50])
        with col1:
            st.markdown('#')
            st.markdown('#')
            st.write('#### :blue[存活機率] ####')
        with col2:
            prediction = predict_plot(hr1, hr2, st.session_state['showblue'], st.session_state['showred'], show_label=False)
            print('blue/red: ', st.session_state['showblue'],  st.session_state['showred'])
            st.pyplot(prediction)
            col1, col2, col3 = st.columns(3)
            with col2:
                st.write('#### :blue[開始使用健安心之後 (年)] ####')

    # place the holder here
    enter_col1, enter_col2 = st.columns(2)

    # Hight, weight and BMI
    with st.expander(':man-frowning: :violet[基礎狀態]'):
        age = st.number_input('###### 年齡 ######', step=1, key='age_pred', value=None)

        if age is None:
            age = 65

        bmi = 0
        col1, col1_1, col2, col2_2 = st.columns([5, 2, 5, 2])
        with col1_1:
            height_unit = st.selectbox("###### 身高單位 ######", ["cm", "in"], key='hight-unit_pred')
        with col2_2:
            weight_unit = st.selectbox("###### 體重單位 ######", ["kg", "lbs"], key='weight-unit_pred')
        with col1:
            height = st.number_input('###### 身高 ######', step=1, value=None, key='height_pred')
            if height:
                if height_unit == "in":
                    height = height * 2.54
        with col2:
            weight = st.number_input('###### 體重 ######', step=0.01, value=None, key='weight_pred')
            if weight:
                if weight_unit == "lbs":
                    weight = weight * 0.45359237
        if height and weight:
            bmi = round(weight / ((height / 100) ** 2), 2)
            st.session_state['bmi'] = bmi
        else:
            st.session_state['bmi'] = 28

        col1, col2, col3 = st.columns([3, 3, 4])
        with col1:
            st.markdown('###### 身體質量指數: ######')
            with col2:
                if bmi is not None:
                    st.write('###### ' + str(bmi) + ' ######')

    with st.expander("😷 :blue[病況]"):

        col1, col2 = st.columns(2)
        with col1:
            nyha_display = st.selectbox('###### 紐約心臟學會功能分級 ######', [['None/Unclassified', 0],
                                                                 ['第一級 (沒有心臟衰竭症狀): 沒有身體活動上的限制，日常生活不會引起症狀發生，如過度疲倦、心悸、呼吸困難或心絞痛的症狀。', 1],
                                                                 ['第二級(體力活動輕度受限，伴隨輕微症狀): 休息時會緩解，但從事日常活動(如爬樓梯、掃地)時會出現症狀。', 2],
                                                                 ['第三級(體力活動明顯受限，伴隨中度症狀): 休息時會緩解，但從事輕微活動(如刷牙)時會出現症狀。', 3],
                                                                 ['第四級(不能從事任何體力活動，伴隨嚴重症狀): 無法執行任何身體活動，在休息狀態下就會出現症狀', 4]], format_func=lambda x: x[0],
                                        help='NYHA: New York Heart Association functional classification', index=0)
            nyha = nyha_display[1]
            paod_diplay = st.selectbox('###### 周邊動脈阻塞 ######', [['是', 1], ['否', 0]], format_func=lambda x: x[0], index=1, help='PAOD: Peripheral Arterial Occlusive Disease')
            paod = paod_diplay[1]
        with col2:
            dialysis_display = st.selectbox('###### 洗腎 ######', [['是', 1], ['否', 0]], format_func=lambda x: x[0], index=1)
            dialysis = dialysis_display[1]

    # st.write('---')
    with st.expander(':pill: 心血管保護用藥'):
        col1, col2 = st.columns([5, 2])
        with col1:
            acei_display = st.selectbox('###### 血管收縮素轉化酶抑制劑/血管收縮素第二型受體阻斷劑 ######',
                                        ['無', '得安穩(valsartan)', '可悅您(losartan)', '血樂平(captopril)', '欣保(enalapril)', '心達舒(ramipril)', '非上述藥物'],
                                        help='ACEI/ARB: Angiotensin Converting Enzyme Inhibitors/Angiotensin Receptor Blockers', index=0)
        with col2:
            acei_dose = st.number_input('###### 劑量(mg) ######', disabled=(acei_display == 'None' or acei_display == 'Not mentioned above'), value=None, key='acei_dose_pred')
            if acei_dose:
                if acei_display == '得安穩(valsartan)':
                    total_acei = acei_dose
                elif acei_display == '可悅您(losartan)' or acei_display == '血樂平(captopril)':
                    total_acei = acei_dose * 32 / 15
                elif acei_display == '欣保(enalapril)':
                    total_acei = acei_dose * 16
                elif acei_display == '心達舒(ramipril)':
                    total_acei = acei_dose * 32
                else:
                    total_acei = 0
            else:
                total_acei = 80

        col1, col2 = st.columns(2)
        with col1:
            en_h_display = st.selectbox('###### 打算什麼時候用健安心 ######',
                                        ['門診啟用(OPD)', '住院啟用(IPD)', 'None'], key='en_h_display_pred', index=0)
        with col2:
            ua_u_o_display = st.selectbox('###### 降尿酸藥 ######', ['無', '欣律(allopurinol)', '優力康(benzbromarone)', '福避痛(febuxostat)', 'probenecid', '法舒克(rasburicase)', '速復利(sulfinpyrazone)', '非上述藥物'], index=0)
            if ua_u_o_display == '無' or ua_u_o_display == '非上述藥物':
                ua_u_0 = 0
            else:
                ua_u_0 = 1
        col1, col2 = st.columns(2)
        with col1:
            p2y12_display = st.selectbox('###### P2Y12 血小板抑制劑 ######', ['None', 'clopidogrel', 'prasugrel', 'ticagrelor', 'Not mentioned above'], index=0, key='p2y12_display_pred')
            if p2y12_display == 'None' or p2y12_display == 'Not mentioned above':
                p2y12 = 0
            else:
                p2y12 = 1

    with st.expander('🩸 :orange[抽血報告]'):
        with st.container():
            col1, col1_1, space, col2, col3 = st.columns([3, 6, 3, 3, 6])
            with col1:
                st.write(f'###### 血中尿素氮(腎功能 ######')
                bun_none = st.checkbox('None', key='bun_none_pred', value=True)
            with col1_1:
                bun = st.number_input('(mg/dL)', disabled=bun_none, help='BUN: Blood Urea Nitrogen', value=None, key='bun_pred', format="%0.2f")

            if bun is None:
                bun = 30

            with col2:
                st.write(f'###### 心臟衰竭指數 ######')
                nt_proBNP_none = st.checkbox('None', key='nt_proBNP_none_pred', value=True)
            with col3:
                nt_proBNP = st.number_input('(pg/mL)', disabled=nt_proBNP_none, help='NT-proBNP: N-Terminal Pro-Brain (or B-type) Natriuretic Peptide', value=None, key='nt_proBNP_pred', format="%0.2f")

            if nt_proBNP is None:
                nt_proBNP = 1500

        st.write(' ')

        with st.container():
            col1, col1_1, space1, col2, col2_1 = st.columns([3, 6, 3, 3, 6])
            with col1:
                st.write(f'###### 丙胺酸轉胺酶(肝功能) ######')
                alt_none = st.checkbox('None', key='alt_none_pred', value=True)
            with col1_1:
                alt = st.number_input('(U/L)', disabled=alt_none, key='alt_pred', help='ALT: Alanine Aminotransferase', value=None, format="%0.2f")

            if alt is None:
                alt = 30

            with col2:
                st.write(f'###### 紅血球大小變異係數(發炎相關指數) ######')
                rdw_cv_none = st.checkbox('None', key='rdw_cv_none_pred', value=True)
            with col2_1:
                rdw_cv = st.number_input('(%)', disabled=rdw_cv_none, key='rdw_cv_pred', help='RDW-CV: Red Cell Distribution Width_Coefficient of Variation', value=None, format="%0.2f")

            if rdw_cv is None:
                rdw_cv = 14.5

    with st.expander('❤️ :red[心臟超音波報告]'):
        with st.container():
            col1, col1_1, space1, col2, col2_1 = st.columns([3, 6, 3, 3, 6])
            with col1:
                st.write(f'###### 主動脈瓣逆流程度 ######')
                ar_none = st.checkbox('None', key='ar_none_pred', value=True)
            with col1_1:
                ar = st.selectbox(' ', [['trace/trivial', 0.5], ['mild', 1], ['mild to moderate', 1.5], ['moderate', 2],
                                        ['moderate to severe', 2.5], ['severe', 3]], label_visibility='visible', disabled=ar_none, help='AR: Aortic Regurgitation', format_func=lambda x: x[0], key='ar_pred', index=2)
                ar_value = ar[1]
            with col2:
                st.write(f'###### 右心室大小 ######')
                rvdd_none = st.checkbox('None', key='rvdd_none_pred', value=True)
            with col2_1:
                rvdd = st.number_input('(cm)', key='rvdd_pred', disabled=rvdd_none, help='RV: RVDd, Right Ventricular Diastolic Dimension', value=None, format="%0.2f")

            if rvdd is None:
                rvdd = 3.2

        with st.container():
            col1, col1_1, space1, col2, col2_1 = st.columns([3, 6, 3, 3, 6])
            with col1:
                st.write(f'###### 心室中膈厚度 ######')
                ivsd_none = st.checkbox('None', key='ivsd_none_pred', value=True)
            with col1_1:
                ivsd = st.number_input('(cm)', key='ivsd_pred', disabled=ivsd_none, help='IVSd: Interventricular Septum Dimension', value=None, format="%0.2f")

            if ivsd is None:
                ivsd = 1.2

            with col2:
                st.write(f'###### 左心室重量指數 ######')
                lvmi_none = st.checkbox('None', key='lvmi_none_pred', value=True)
            with col2_1:
                lvmi = st.number_input('(g/m2)', key='lvmi_pred', disabled=lvmi_none, label_visibility='visible', help='LVMI: Left Ventricular Mass Index', value=None, format="%0.2f")

            if lvmi is None:
                lvmi = 12.5

        with st.container():
            col1, col1_1, space1, col2, col2_1 = st.columns([3, 6, 3, 3, 6])
            with col1:
                st.write(f'###### 心臟收縮時的大小 ######')
                esd_none = st.checkbox('None', key='esd_none_pred', value=True)
            with col1_1:
                esd = st.number_input('(cm)', key='esd_pred', disabled=esd_none, help='ESD: End Systolic Dimension = LVIDs, Left Ventricular Internal Diameter End Systole', value=None, format="%0.2f")

            if esd is None:
                esd = 5.5

            with col2:
                st.write(f'###### 左心房大小 ######')
                lad_none = st.checkbox('None', key='lad_none_pred', value=True)
            with col2_1:
                lad = st.number_input('(cm)', key='lad_pred', disabled=lad_none, label_visibility='visible', help='LAD, Left Atrial Diameter', value=None, format="%0.2f")

            if lad is None:
                lad = 4.5

        with st.container():
            col1, col1_1, space1, col2, col2_1 = st.columns([3, 6, 3, 3, 6])
            with col1:
                st.write(f'###### 左心室射血比例 ######')
                lvef_2d_none = st.checkbox('None', key='lvef_2d_none_pred', value=True)
            with col1_1:
                lvef_2d = st.number_input('(%)', key='lvef_2d_pred', disabled=lvef_2d_none, label_visibility='visible', help='LVEF_2D: Left Ventricular Ejection Fraction_2D = EF MOD-sp4, Ejection Fraction Method of Disks-Single Plane, Apical 4 Chamber', value=None, format="%0.2f")

            if lvef_2d is None:
                lvef_2d = 30


    # Assign what shall do in enter_col1 and enter_col2
    st.markdown("""
<style>.element-container:has(#button-col1) + div button {
 background-color: #0000ff;
        color: #ffffff;
 }</style>""", unsafe_allow_html=True)
    with enter_col1:
        st.markdown('<span id="button-col1"></span>', unsafe_allow_html=True)
        left_button = st.button('輸入', 'enter1_pred', on_click=calculate_and_set, args=(
            dialysis, bun, age, lvef_2d_none, lvef_2d, esd_none, esd, rdw_cv_none, rdw_cv, ivsd_none, ivsd, bmi, lvmi_none, lvmi, nt_proBNP_none, nt_proBNP, paod, total_acei, p2y12, ar_none, ar_value, en_h_display, nyha, rvdd_none, rvdd, ua_u_0, alt_none, alt, lad_none, lad, 'risk_value_col1_pred'),
                  type='primary')

    st.markdown("""
<style>.element-container:has(#button-col2) + div button {
 background-color: #ff0000;
        color: #ffffff;
 }</style>""", unsafe_allow_html=True)
    with enter_col2:
        st.markdown('<span id="button-col2"></span>', unsafe_allow_html=True)
        right_button = st.button('輸入', 'enter2_pred', on_click=calculate_and_set, args=(
            dialysis, bun, age, lvef_2d_none, lvef_2d, esd_none, esd, rdw_cv_none, rdw_cv, ivsd_none, ivsd, bmi, lvmi_none, lvmi, nt_proBNP_none, nt_proBNP, paod, total_acei, p2y12, ar_none, ar_value, en_h_display, nyha, rvdd_none, rvdd, ua_u_0, alt_none, alt, lad_none, lad, 'risk_value_col2_pred'),
                  type='secondary')

    if left_button:
        st.session_state['showblue'] = True
        st.experimental_rerun()
    if right_button:
        st.session_state['showred'] = True
        st.experimental_rerun()

    copy_explain_btn = st.button('Copy from Explanation')
    if copy_explain_btn:
        st.session_state['pred_copy'] = True
        st.session_state['showblue'] = True
        st.session_state['showred'] = True
        st.experimental_rerun()


def prediction_view_en():
    st.subheader('Survival Prediction')
    # Set "pred_copy" related controls
    if "pred_copy" not in st.session_state:
        # If baseline and prediction all not input
        st.session_state['pred_copy'] = False

    # If copy from explanation is activated
    if st.session_state['pred_copy']:
        # blue copy if there's value in baseline model
        if 'risk_value_col1' in st.session_state:
            hr1 = st.session_state['risk_value_col1']
            st.session_state['risk_value_col1_pred'] = hr1
        # blue set to 1 if copy from baseline clicked but baseline not set
        else:
            hr1 = 1
            st.session_state['risk_value_col1_pred'] = hr1

        if 'risk_value_col2' in st.session_state:
            hr2 = st.session_state['risk_value_col2']
            st.session_state['risk_value_col2_pred'] = hr2
        else:
            hr2 = 1
            st.session_state['risk_value_col2_pred'] = hr2

    # If copy from explanation is not activated
    else:
        if 'risk_value_col1_pred' not in st.session_state:
            st.session_state['risk_value_col1_pred'] = HrControl.risk_calculation()
            hr1 = st.session_state['risk_value_col1_pred']

        else:
            hr1 = st.session_state['risk_value_col1_pred']

        if 'risk_value_col2_pred' not in st.session_state:
            st.session_state['risk_value_col2_pred'] = 1.0
            hr2 = st.session_state['risk_value_col2_pred']
        else:
            hr2 = st.session_state['risk_value_col2_pred']

    # Determine if showblue or showred button is clicked
    if 'showblue' not in st.session_state:
        st.session_state['showblue'] = False
    if 'showred' not in st.session_state:
        st.session_state['showred'] = False

    # plotting
    prediction = predict_plot(hr1, hr2, st.session_state['showblue'], st.session_state['showred'])
    print('blue/red: ', st.session_state['showblue'],  st.session_state['showred'])
    st.pyplot(prediction)

    # place the holder here
    enter_col1, enter_col2 = st.columns(2)

    # Hight, weight and BMI
    with st.expander(':man-frowning: :violet[Baseline status]'):
        age = st.number_input('###### Age ######', step=1, key='age_pred', value=None)

        if age is None:
            age = 65

        bmi = 0
        col1, col1_1, col2, col2_2 = st.columns([5, 2, 5, 2])
        with col1_1:
            height_unit = st.selectbox("###### Height_unit ######", ["cm", "in"], key='hight-unit_pred')
        with col2_2:
            weight_unit = st.selectbox("###### Weight_unit ######", ["kg", "lbs"], key='weight-unit_pred')
        with col1:
            height = st.number_input('###### Height ######', step=1, value=None, key='height_pred')
            if height:
                if height_unit == "in":
                    height = height * 2.54
        with col2:
            weight = st.number_input('###### Weight ######', step=0.01, value=None, key='weight_pred')
            if weight:
                if weight_unit == "lbs":
                    weight = weight * 0.45359237
        if height and weight:
            bmi = round(weight / ((height / 100) ** 2), 2)
            st.session_state['###### bmi ######'] = bmi
        else:
            st.session_state['bmi'] = 28

        col1, col2, col3 = st.columns([1, 3, 4])
        with col1:
            st.markdown('###### BMI: ######')
            with col2:
                if bmi is not None:
                    st.write('###### ' + str(bmi) + ' ######')

    with st.expander("😷 :blue[Disease status]"):

        col1, col2 = st.columns(2)
        with col1:
            nyha_display = st.selectbox('###### NYHA ######', [['None/Unclassified', 0],
                                                 ['Class I (No limitation of physical activity. Ordinary physical activity does not cause undue fatigue, palpitation or shortness of breath.)', 1],
                                                 ['Class II (Slight limitation of physical activity. Comfortable at rest. Ordinary physical activity results in fatigue, palpitation, shortness of breath or chest pain.)', 2],
                                                 ['Class III (Marked limitation of physical activity. Comfortable at rest. Less than ordinary activity causes fatigue, palpitation, shortness of breath or chest pain.)', 3],
                                                 ['Class IV (Symptoms of heart failure at rest. Any physical activity causes further discomfort.)', 4]], format_func=lambda x: x[0],
                                        help='New York Heart Association functional classification', index=2, key='nyha_display_pred')
            nyha = nyha_display[1]
            paod_diplay = st.selectbox('###### PAOD ######', [['yes', 1], ['no', 0]], format_func=lambda x: x[0], index=1, help='Peripheral Arterial Occlusive Disease', key='paod_diplay_pred')
            paod = paod_diplay[1]
        with col2:
            dialysis_display = st.selectbox('###### Dialysis ######', [['yes', 1], ['no', 0]], format_func=lambda x: x[0], index=1, key='dialysis_display_pred')
            dialysis = dialysis_display[1]

    # st.write('---')
    with st.expander(':pill: Drug use'):
        col1, col2 = st.columns([5, 2])
        with col1:
            acei_display = st.selectbox('###### ACEI/ARB ######',
                                        ['None', 'Valsartan', 'Losartan', 'Captopril', 'Enalapril', 'Ramipril', 'Not mentioned above'],
                                        help='Angiotensin Converting Enzyme Inhibitors/Angiotensin Receptor Blockers', index=1, key='acei_display_pred')
        with col2:
            acei_dose = st.number_input('###### Dose(mg) ######', disabled=(acei_display == 'None' or acei_display == 'Not mentioned above'), value=None, key='acei_dose_pred')
            if acei_dose:
                if acei_display == 'Valsartan':
                    total_acei = acei_dose
                elif acei_display == 'Losartan' or acei_display == 'Captopril':
                    total_acei = acei_dose * 32 / 15
                elif acei_display == 'Enalapril':
                    total_acei = acei_dose * 16
                elif acei_display == 'Ramipril':
                    total_acei = acei_dose * 32
                else:
                    total_acei = 0
            else:
                total_acei = 80

        col1, col2 = st.columns(2)
        with col1:
            en_h_display = st.selectbox('###### Initiation time of Entresto(sacubitril/valsartan) ######',
                                        ['Outpatient Department (OPD)', 'Inpatient Department (IPD)', 'None'], key='en_h_display_pred', index=0)
        with col2:
            ua_u_o_display = st.selectbox('###### Urate-lowering Agents ######', ['None', 'allopurinol', 'benzbromarone', 'febuxostat', 'probenecid', 'rasburicase', 'sulfinpyrazone', 'Not mentioned above'], index=0, key='ua_u_o_display_pred')
            if ua_u_o_display == 'None' or ua_u_o_display == 'Not mentioned above':
                ua_u_0 = 0
            else:
                ua_u_0 = 1
        col1, col2 = st.columns(2)
        with col1:
            p2y12_display = st.selectbox('###### P2Y12 Receptor Inhibitors ######', ['None', 'clopidogrel', 'prasugrel', 'ticagrelor', 'Not mentioned above'], index=0, key='p2y12_display_pred')
            if p2y12_display == 'None' or p2y12_display == 'Not mentioned above':
                p2y12 = 0
            else:
                p2y12 = 1

    with st.expander('🩸 :orange[Lab data]'):
        with st.container():
            col1, col1_1, space, col2, col3 = st.columns([3, 6, 3, 3, 6])
            with col1:
                st.write(f'###### BUN ######')
                bun_none = st.checkbox('None', key='bun_none_pred', value=True)
            with col1_1:
                bun = st.number_input('(mg/dL)', disabled=bun_none, help='Blood Urea Nitrogen', value=None, key='bun_pred', format="%0.2f")

            if bun is None:
                bun = 30

            with col2:
                st.write(f'###### NT-proBNP ######')
                nt_proBNP_none = st.checkbox('None', key='nt_proBNP_none_pred', value=True)
            with col3:
                nt_proBNP = st.number_input('(pg/mL)', disabled=nt_proBNP_none, help='N-Terminal Pro-Brain (or B-type) Natriuretic Peptide', value=None, key='nt_proBNP_pred', format="%0.2f")

            if nt_proBNP is None:
                nt_proBNP = 1500

        st.write(' ')

        with st.container():
            col1, col1_1, space1, col2, col2_1 = st.columns([3, 6, 3, 3, 6])
            with col1:
                st.write(f'###### ALT ######')
                alt_none = st.checkbox('None', key='alt_none_pred', value=True)
            with col1_1:
                alt = st.number_input('(U/L)', disabled=alt_none, key='alt_pred', help='Alanine Aminotransferase', value=None, format="%0.2f")

            if alt is None:
                alt = 30

            with col2:
                st.write(f'###### RDW-CV ######')
                rdw_cv_none = st.checkbox('None', key='rdw_cv_none_pred', value=True)
            with col2_1:
                rdw_cv = st.number_input('(%)', disabled=rdw_cv_none, key='rdw_cv_pred', help='Red Cell Distribution Width_Coefficient of Variation', value=None, format="%0.2f")

            if rdw_cv is None:
                rdw_cv = 14.5

    with st.expander('❤️ :red[Cardiac parameters of echocardiography]'):
        with st.container():
            col1, col1_1, space1, col2, col2_1 = st.columns([3, 6, 3, 3, 6])
            with col1:
                st.write(f'###### AR ######')
                ar_none = st.checkbox('None', key='ar_none_pred', value=True)
            with col1_1:
                ar = st.selectbox(' ', [['trace/trivial', 0.5], ['mild', 1], ['mild to moderate', 1.5], ['moderate', 2],
                                        ['moderate to severe', 2.5], ['severe', 3]], label_visibility='visible', disabled=ar_none, help='Aortic Regurgitation', format_func=lambda x: x[0], key='ar_pred', index=2)
                ar_value = ar[1]
            with col2:
                st.write(f'###### RV ######')
                rvdd_none = st.checkbox('None', key='rvdd_none_pred', value=True)
            with col2_1:
                rvdd = st.number_input('(cm)', key='rvdd_pred', disabled=rvdd_none, help='RVDd, Right Ventricular Diastolic Dimension', value=None, format="%0.2f")

            if rvdd is None:
                rvdd = 3.2

        with st.container():
            col1, col1_1, space1, col2, col2_1 = st.columns([3, 6, 3, 3, 6])
            with col1:
                st.write(f'###### IVSd ######')
                ivsd_none = st.checkbox('None', key='ivsd_none_pred', value=True)
            with col1_1:
                ivsd = st.number_input('(cm)', key='ivsd_pred', disabled=ivsd_none, help='Interventricular Septum Dimension', value=None, format="%0.2f")

            if ivsd is None:
                ivsd = 1.2

            with col2:
                st.write(f'###### LVMI ######')
                lvmi_none = st.checkbox('None', key='lvmi_none_pred', value=True)
            with col2_1:
                lvmi = st.number_input('(g/m2)', key='lvmi_pred', disabled=lvmi_none, label_visibility='visible', help='Left Ventricular Mass Index', value=None, format="%0.2f")

            if lvmi is None:
                lvmi = 12.5

        with st.container():
            col1, col1_1, space1, col2, col2_1 = st.columns([3, 6, 3, 3, 6])
            with col1:
                st.write(f'###### ESD ######')
                esd_none = st.checkbox('None', key='esd_none_pred', value=True)
            with col1_1:
                esd = st.number_input('(cm)', key='esd_pred', disabled=esd_none, help='End Systolic Dimension = LVIDs, Left Ventricular Internal Diameter End Systole', value=None, format="%0.2f")

            if esd is None:
                esd = 5.5

            with col2:
                st.write(f'###### LAD ######')
                lad_none = st.checkbox('None', key='lad_none_pred', value=True)
            with col2_1:
                lad = st.number_input('(cm)', key='lad_pred', disabled=lad_none, label_visibility='visible', help='LAD, Left Atrial Diameter', value=None, format="%0.2f")

            if lad is None:
                lad = 4.5

        with st.container():
            col1, col1_1, space1, col2, col2_1 = st.columns([3, 6, 3, 3, 6])
            with col1:
                st.write(f'###### LVEF_2D ######')
                lvef_2d_none = st.checkbox('None', key='lvef_2d_none_pred', value=True)
            with col1_1:
                lvef_2d = st.number_input('(%)', key='lvef_2d_pred', disabled=lvef_2d_none, label_visibility='visible', help='Left Ventricular Ejection Fraction_2D = EF MOD-sp4, Ejection Fraction Method of Disks-Single Plane, Apical 4 Chamber', value=None, format="%0.2f")

            if lvef_2d is None:
                lvef_2d = 30


    # Assign what shall do in enter_col1 and enter_col2
    st.markdown("""
<style>.element-container:has(#button-col1) + div button {
 background-color: #0000ff;
        color: #ffffff;
 }</style>""", unsafe_allow_html=True)
    with enter_col1:
        st.markdown('<span id="button-col1"></span>', unsafe_allow_html=True)
        left_button = st.button('Enter', 'enter1_pred', on_click=calculate_and_set, args=(
            dialysis, bun, age, lvef_2d_none, lvef_2d, esd_none, esd, rdw_cv_none, rdw_cv, ivsd_none, ivsd, bmi, lvmi_none, lvmi, nt_proBNP_none, nt_proBNP, paod, total_acei, p2y12, ar_none, ar_value, en_h_display, nyha, rvdd_none, rvdd, ua_u_0, alt_none, alt, lad_none, lad, 'risk_value_col1_pred'),
                  type='primary')

    st.markdown("""
<style>.element-container:has(#button-col2) + div button {
 background-color: #ff0000;
        color: #ffffff;
 }</style>""", unsafe_allow_html=True)
    with enter_col2:
        st.markdown('<span id="button-col2"></span>', unsafe_allow_html=True)
        right_button = st.button('Enter', 'enter2_pred', on_click=calculate_and_set, args=(
            dialysis, bun, age, lvef_2d_none, lvef_2d, esd_none, esd, rdw_cv_none, rdw_cv, ivsd_none, ivsd, bmi, lvmi_none, lvmi, nt_proBNP_none, nt_proBNP, paod, total_acei, p2y12, ar_none, ar_value, en_h_display, nyha, rvdd_none, rvdd, ua_u_0, alt_none, alt, lad_none, lad, 'risk_value_col2_pred'),
                  type='secondary')

    if left_button:
        st.session_state['showblue'] = True
        st.experimental_rerun()
    if right_button:
        st.session_state['showred'] = True
        st.experimental_rerun()

    copy_explain_btn = st.button('Copy from Explanation')
    if copy_explain_btn:
        st.session_state['pred_copy'] = True
        st.session_state['showblue'] = True
        st.session_state['showred'] = True
        st.experimental_rerun()


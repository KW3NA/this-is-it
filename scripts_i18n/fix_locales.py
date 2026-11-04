#!/usr/bin/env python3
# Fixes missing i18n keys in af.ts / zu.ts and adds auth.dontHaveAccount to the other locales.
import re, os, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.chdir(ROOT)

AF = {
  'auth.dontHaveAccount': "Het jy nog nie 'n rekening nie?",
  'assessment.previous': 'Vorige',
  'assessment.nextButton': 'Volgende',
  'assessment.submitAssessment': 'Dien assessering in',
  'assessment.submitConfirmBody': 'Is jy seker jy wil jou assessering indien?',
  'assessment.quitTitle': 'Verlaat assessering?',
  'assessment.quitBody': 'Is jy seker jy wil verlaat? Jou vordering sal verlore wees.',
  'assessment.quit': 'Verlaat',
  'assessment.trueLabel': 'Waar',
  'assessment.falseLabel': 'Onwaar',
  'assessment.typeAnswerPlaceholder': 'Tik jou antwoord hier...',
  'assessment.noQuestions': 'Daar is geen vrae beskikbaar vir hierdie assessering nie.',
  'assessment.q1_1': 'Wat beteken "blaai" op die internet?',
  'assessment.q1_1_opt0': 'Deur webbladsye beweeg',
  'assessment.q1_1_opt1': "'n Foto neem",
  'assessment.q1_1_opt2': 'Jou foon afskakel',
  'assessment.q1_1_opt3': "'n E-pos stuur",
  'assessment.q1_2': 'Wat is \'n webblaaier?',
  'assessment.q1_3': 'Waarom moet jy versigtig wees met e-posskakels?',
  'assessment.q1_4': 'Watter van hierdie is \'n veilige wagwoord?',
  'assessment.q1_4_opt0': '123456',
  'assessment.q1_4_opt1': 'password',
  'assessment.q1_4_opt2': 'K9$mZ!x2pQ',
  'assessment.q1_4_opt3': 'jou geboortedatum',
  'assessment.q1_5': 'Wat is die internet?',
  'assessment.q2_1': 'Watter app gebruik jy gewoonlik om boodskappe te stuur?',
  'assessment.q2_2': 'Wat beteken "download"?',
  'assessment.q2_2_opt0': 'Inligting van die internet afhaal',
  'assessment.q2_2_opt1': 'Inligting na die internet oplaai',
  'assessment.q2_2_opt2': 'Jou foon herstel',
  'assessment.q2_2_opt3': "'n App verwyder",
  'assessment.q2_3': 'Hoe kan jy jou aanlyn rekening beveilig?',
  'assessment.q2_4': 'Watter een is \'n voorbeeld van \'n sosialemediatoepassing?',
  'assessment.q2_4_opt0': 'Facebook',
  'assessment.q2_4_opt1': 'Rekenaar',
  'assessment.q2_4_opt2': 'Kamera',
  'assessment.q2_4_opt3': 'Sakrekenaar',
  'assessment.q3_1': 'Watter formaat is algemeen vir CV-documente?',
  'assessment.q3_1_opt0': 'PDF',
  'assessment.q3_1_opt1': 'MP3',
  'assessment.q3_1_opt2': 'JPG',
  'assessment.q3_1_opt3': 'ZIP',
  'assessment.q3_2': 'Wat moet bo-aan jou CV verskyn?',
  'assessment.q3_3': "Hoekom is jou e-posadres belangrik op 'n CV?",
  'assessment.q3_4': 'Watter van hierdie moenie op jou CV ingesluit word nie?',
  'assessment.q3_4_opt0': 'Jou salarisverwagting as privaat inligting',
  'assessment.q3_4_opt1': 'Jou werksgeskiedenis',
  'assessment.q3_4_opt2': 'Jou kontakbesonderhede',
  'assessment.q3_4_opt3': 'Jou vaardighede',
  'assessment.q4_1': 'Wat is "cibervloekery"?',
  'assessment.q4_1_opt0': 'Die gebruik van tegnologie om iemand te teiken of te laster',
  'assessment.q4_1_opt1': 'Iemand fisies seer maak',
  'assessment.q4_1_opt2': "Diefstal van 'n foon",
  'assessment.q4_1_opt3': 'Te veel tyd op sosiale media spandeer',
  'assessment.q4_2': 'Wat moet jy doen as jy aanlyn getreiter word?',
  'assessment.q4_3': 'Wat is \'n "wagter" (guardian) in die konteks van aanlynveiligheid?',
  'assessment.q4_4': 'Watter gedrag help om aanlyn veilig te bly?',
  'assessment.q4_4_opt0': 'Deel jou wagwoord met vertroue vriende',
  'assessment.q4_4_opt1': 'Klik op elke skakel wat jy ontvang',
  'assessment.q4_4_opt2': 'Wees versigtig met persoonlike inligting wat jy deel',
  'assessment.q4_4_opt3': 'Gebruik dieselfde wagwoord oral',
  'assessment.q5_1': "Wat is 'n e-posbylaag?",
  'assessment.q5_2': 'Watter van hierdie is VEILIGE wagwoordpraktyke?',
  'assessment.q5_2_opt0': "Gebruik 'n unieke wagwoord vir elke rekening",
  'assessment.q5_2_opt1': 'Gebruik "123456"',
  'assessment.q5_2_opt2': 'Jou wagwoord met kollegas deel',
  'assessment.q5_2_opt3': "Jou wagwoord op 'n plakkertjie by jou rekenaar skryf",
  'assessment.q5_3': 'Wat beteken "phishing"?',
  'assessment.q6_1': 'Wat is die eerste stap om \'n e-posadres te kry?',
  'assessment.q6_1_opt0': "Registreer by 'n e-posdiens soos Gmail of Outlook",
  'assessment.q6_1_opt1': "'n Foon koop",
  'assessment.q6_1_opt2': 'Na die winkel toe gaan',
  'assessment.q6_1_opt3': "Iemand anders se e-pos gebruik",
  'assessment.q6_2': 'Watter van hierdie moet JY NOOIT per e-pos stuur nie?',
  'assessment.q6_3': 'Wat is die voordeel van e-bankiersake?',
  'assessment.quiz_cv_q1': 'Wat staan CV kort vir?',
  'assessment.quiz_cv_q1_opt0': 'Curriculum Vitae',
  'assessment.quiz_cv_q1_opt1': 'Certificate of Value',
  'assessment.quiz_cv_q1_opt2': 'Career Vision',
  'assessment.quiz_cv_q1_opt3': 'Company Verification',
  'assessment.quiz_cv_q2': 'Watter insluite behoort in jou CV te wees?',
  'assessment.quiz_cv_q2_opt0': 'Jou werksgeskiedenis en vaardighede',
  'assessment.quiz_cv_q2_opt1': 'Jou gunsteling kos',
  'assessment.quiz_cv_q2_opt2': 'Jou familiegeskiedenis',
  'assessment.quiz_cv_q2_opt3': 'Jou hobby\'s alleen',
  'assessment.quiz_cv_q3': 'Hoekom is dit belangrik om jou CV op te dateer?',
  'assessment.quiz_cv_q3_opt0': 'Om onlangse ervarings en vaardighede te wys',
  'assessment.quiz_cv_q3_opt1': 'Om papier te spaar',
  'assessment.quiz_cv_q3_opt2': 'Dit hoef nooit opgedateer te word nie',
  'assessment.quiz_cv_q3_opt3': 'Net vir universiteitsaansoeke',
  'assessment.quiz_safety_q1': 'Wat is \'n veilige manier om \'n wagwoord te kies?',
  'assessment.quiz_safety_q1_opt0': "'n Kombinasy van letters, syfers en simbole",
  'assessment.quiz_safety_q1_opt1': 'Jou geboortedatum',
  'assessment.quiz_safety_q1_opt2': '"password"',
  'assessment.quiz_safety_q1_opt3': 'Jou naam',
  'assessment.quiz_safety_q2': 'Wat moet jy doen as jy \'n verdagte e-pos ontvang?',
  'assessment.quiz_safety_q2_opt0': 'Merk dit as spam/versigtigheid en moenie skakels klik',
  'assessment.quiz_safety_q2_opt1': 'Antwoord onmiddellik',
  'assessment.quiz_safety_q2_opt2': 'Aanstuur aan al jou kontakte',
  'assessment.quiz_safety_q2_opt3': 'Gee jou wagwoord in',
  'assessment.quiz_safety_q3': 'Wanneer moet jy jou persoonlike inligting online deel?',
  'assessment.quiz_safety_q3_opt0': 'Net met vertroude, veilige dienste',
  'assessment.quiz_safety_q3_opt1': 'Altyd met almal',
  'assessment.quiz_safety_q3_opt2': 'Op enige webwerf',
  'assessment.quiz_safety_q3_opt3': 'Nooit met jou bank',
  'loginScreen.subtitle': 'Bemagtig Digitale Toekoms',
  'loginScreen.logInTab': 'Meld aan',
  'loginScreen.signUpTab': 'Registreer',
  'loginScreen.sendOtp': 'Stuur OTP',
  'loginScreen.continueBtn': 'Gaan voort',
  'loginScreen.registerWithEmail': 'Registreer met e-pos',
  'loginScreen.registerWithPhone': 'Registreer met foonnommer',
  'loginScreen.loginWithEmail': 'Meld aan met e-pos',
  'loginScreen.loginWithPhone': 'Meld aan met foonnommer',
  'loginScreen.or': 'of',
  'loginScreen.createAccount': 'Skep rekening',
  'loginScreen.alreadyHaveAccountLogin': 'Het jy reeds \'n rekening?',
  'loginScreen.loginLink': 'Meld aan',
  'loginScreen.orLoginWith': 'Of meld aan met',
  'loginScreen.rememberMe': 'Onthou my',
  'loginScreen.maintenanceTitle': 'Onder instandhouding',
  'loginScreen.maintenanceMessage': 'Ons bedieners is tans onder instandhouding. Probeer asseblief later weer.',
  'loginScreen.enterValidPhone': "Voer asseblief 'n geldige foonnommer in",
  'loginScreen.enterName': 'Voer asseblief jou naam in',
  'loginScreen.minPassword': 'Wagwoord moet ten minste 6 karakters wees',
  'loginScreen.failedToSendCode': 'Kon nie die bevestigingskode stuur nie',
  'loginScreen.phoneAuthFailed': 'Kon nie foon-verifikasie hanteer nie',
  'loginScreen.invalidResponse': "Bediener het 'n ongeldige antwoord teruggestuur.",
  'loginScreen.loginFailedTitle': 'Aantekening misluk',
  'loginScreen.checkCredentials': 'Gaaf asseblief jou geloofsbriete na en probeer weer',
  'loginScreen.accountCreated': 'Rekening suksesvol geskep!',
  'loginScreen.signupFailedTitle': 'Registrasie misluk',
  'loginScreen.noToken': "Bediener het nie 'n token teruggegee nie.",
  'loginScreen.tryAgain': 'Probeer asseblief weer',
}

ZU = {
  'auth.dontHaveAccount': 'Awunayo i-akhawunti?',
  'assessment.previous': 'Okwedlule',
  'assessment.nextButton': 'Okulandelayo',
  'assessment.submitAssessment': 'Thumela Uhlolo',
  'assessment.submitConfirmBody': 'Uqinisekile ukuthi ufuna ukuthumela uhlolo lwakho?',
  'assessment.quitTitle': 'Uphuma ehlolweni?',
  'assessment.quitBody': 'Uqinisekile ukuthi ufuna ukuphuma? Inqubekelaphambili yakho izolahleka.',
  'assessment.quit': 'Phuma',
  'assessment.trueLabel': 'Kuyiqiniso',
  'assessment.falseLabel': 'Akuyilo qiniso',
  'assessment.typeAnswerPlaceholder': 'Bhala impendulo yakho lapha...',
  'assessment.noQuestions': 'Azikho imibuzo etholakalayo yalolu hlolo.',
  'assessment.q1_1': 'Yini ukuphequlula ku-inthanethi?',
  'assessment.q1_1_opt0': 'Ukusheqa amakhasi ewebhu',
  'assessment.q1_1_opt1': 'Ukuthwebula isithombe',
  'assessment.q1_1_opt2': 'Ukucisha ifoni',
  'assessment.q1_1_opt3': 'Ukuthumela i-imeyili',
  'assessment.q1_2': 'Yini isiphequluli sewebhu?',
  'assessment.q1_3': 'Kungani kumele uqaphele ezixhumanisini ze-imeyili?',
  'assessment.q1_4': 'Kuliphi kulawa eliyiphasiwedi ephephile?',
  'assessment.q1_4_opt0': '123456',
  'assessment.q1_4_opt1': 'iphasiwedi',
  'assessment.q1_4_opt2': 'K9$mZ!x2pQ',
  'assessment.q1_4_opt3': 'usuku lokuzalwa kwakho',
  'assessment.q1_5': 'Yini i-inthanethi?',
  'assessment.q2_1': 'Yiphi i-app ojwayele ukusebenzisa ukuthumela imilayezo?',
  'assessment.q2_2': 'Yini ukulanda (download)?',
  'assessment.q2_2_opt0': 'Ukulanda ulwazi ku-inthanethi',
  'assessment.q2_2_opt1': 'Ukulayisha ulwazi ku-inthanethi',
  'assessment.q2_2_opt2': 'Ukusetha kabusha ifoni',
  'assessment.q2_2_opt3': 'Ukususa i-app',
  'assessment.q2_3': 'Ungasilivikela kanjani isikhathi sakho se-inthanethi?',
  'assessment.q2_4': 'Iliphi kula eliyisibonelo se-app yenethomthetho yezokuxhumana?',
  'assessment.q2_4_opt0': 'Facebook',
  'assessment.q2_4_opt1': 'Ikhalkhyuleyitha',
  'assessment.q2_4_opt2': 'Ikhamera',
  'assessment.q2_4_opt3': 'Ikhhalenda',
  'assessment.q3_1': 'Yiphi ifomati ejwayelekile yamadokhumenti e-CV?',
  'assessment.q3_1_opt0': 'PDF',
  'assessment.q3_1_opt1': 'MP3',
  'assessment.q3_1_opt2': 'JPG',
  'assessment.q3_1_opt3': 'ZIP',
  'assessment.q3_2': 'Kufanele kube yini phezulu kwe-CV yakho?',
  'assessment.q3_3': 'Kungani ikheli lakho le-imeyili libalulekile ku-CV?',
  'assessment.q3_4': 'Kukuphi okungekufaki ku-CV yakho?',
  'assessment.q3_4_opt0': 'Inoma yakho yomuntu siqu yenkokhelo',
  'assessment.q3_4_opt1': 'Umlando wakho wokusebenza',
  'assessment.q3_4_opt2': 'Imininingwane yakho yokuxhumana',
  'assessment.q3_4_opt3': 'Amakhono akho',
  'assessment.q4_1': 'Yini i-cyberbullying?',
  'assessment.q4_1_opt0': 'Ukusebenzisa ubuchwepheshe kuhloswe umuntu noma kumhlazwaye',
  'assessment.q4_1_opt1': 'Ukulimaza umuntu ngokomzimba',
  'assessment.q4_1_opt2': 'Ukweba ifoni',
  'assessment.q4_1_opt3': 'Ukuchitha isikhathi esiningi emithonjeni yezenhlalo',
  'assessment.q4_2': 'Kufanele wenze yini uma ushaya ngokobudlova benetha?',
  'assessment.q4_3': 'Yini umgcini (guardian) ekuphepheni kwe-inthanethi?',
  'assessment.q4_4': 'Yiphi impilo ezisiza ukuhlala uphephile ku-inthanethi?',
  'assessment.q4_4_opt0': 'Ukwabelana ngephasiwedi nabangane abathembekile',
  'assessment.q4_4_opt1': 'Ukuchofoza zonke izixhumanisi ozitholayo',
  'assessment.q4_4_opt2': 'Ukuqapha ulwazi lomuntu siqu owabelana ngalo',
  'assessment.q4_4_opt3': 'Ukusebenzisa iphasiwedi efanayo yonke indawo',
  'assessment.q5_1': 'Yini isinamathiselo se-imeyili?',
  'assessment.q5_2': 'Yiziphi kulezi izinqubo eziphephile zamaphasiwedi?',
  'assessment.q5_2_opt0': 'Sebenzisa iphasiwedi eyingqayizivele ku-akhawunti ngayinye',
  'assessment.q5_2_opt1': 'Sebenzisa "123456"',
  'assessment.q5_2_opt2': 'Wabelane ngephasiwedi yakho nozakwenu',
  'assessment.q5_2_opt3': 'Bhala iphasiwedi yakho ephepheni elincane',
  'assessment.q5_3': 'Yini i-phishing?',
  'assessment.q6_1': 'Yinyathelo lokuqala lokuthola ikheli le-imeyili?',
  'assessment.q6_1_opt0': 'Zibhalise ensizeni ye-imeyili njenge-Gmail noma i-Outlook',
  'assessment.q6_1_opt1': 'Thenga ifoni',
  'assessment.q6_1_opt2': 'Yiya esitolo',
  'assessment.q6_1_opt3': 'Sebenzisa i-imeyili yomunye umuntu',
  'assessment.q6_2': 'Yini okungafanele UTHUMELE yona nge-imeyili?',
  'assessment.q6_3': 'Yinzuzo yanini yokusebenzisa ibhange le-inthanethi?',
  'assessment.quiz_cv_q1': 'I-CV imele ini?',
  'assessment.quiz_cv_q1_opt0': 'Curriculum Vitae',
  'assessment.quiz_cv_q1_opt1': 'Certificate of Value',
  'assessment.quiz_cv_q1_opt2': 'Career Vision',
  'assessment.quiz_cv_q1_opt3': 'Company Verification',
  'assessment.quiz_cv_q2': 'Yini okufanele ibe khona ku-CV yakho?',
  'assessment.quiz_cv_q2_opt0': 'Umlando wakho wokusebenza namakhono',
  'assessment.quiz_cv_q2_opt1': 'Ukudla okuthandayo',
  'assessment.quiz_cv_q2_opt2': 'Umlando womndeni wakho',
  'assessment.quiz_cv_q2_opt3': 'Amahobhi akho kuphela',
  'assessment.quiz_cv_q3': 'Kungani kubalulekile ukuvuselela i-CV yakho?',
  'assessment.quiz_cv_q3_opt0': 'Ukubonisa ulwazi lwamuva lamava namakhono',
  'assessment.quiz_cv_q3_opt1': 'Ukonga iphepha',
  'assessment.quiz_cv_q3_opt2': 'Ayidingi kuvuselelwa',
  'assessment.quiz_cv_q3_opt3': 'Kuphela ezicellos zenyuvesi',
  'assessment.quiz_safety_q1': 'Yindlela ephephile yokukhetha iphasiwedi?',
  'assessment.quiz_safety_q1_opt0': 'Inhlanganisela yezinhlamvu, izinombolo nezimpawu',
  'assessment.quiz_safety_q1_opt1': 'Usuku lokuzalwa kwakho',
  'assessment.quiz_safety_q1_opt2': '"password"',
  'assessment.quiz_safety_q1_opt3': 'Igama lakho',
  'assessment.quiz_safety_q2': 'Kufanele wenze yini uma uthola i-imeyili ebiselayo?',
  'assessment.quiz_safety_q2_opt0': 'Iphawule njengesiphazamiso ungachofozi izixhumanisi',
  'assessment.quiz_safety_q2_opt1': 'Phendula ngokushesha',
  'assessment.quiz_safety_q2_opt2': 'Yithumele kubo bonke abangani bakho',
  'assessment.quiz_safety_q2_opt3': 'Nika ngephasiwedi yakho',
  'assessment.quiz_safety_q3': 'Nini lapho kufanele wabelane ngolwazi lomuntu siqu ku-inthanethi?',
  'assessment.quiz_safety_q3_opt0': 'Kuphela ngezinsiza ezithembekile nephephile',
  'assessment.quiz_safety_q3_opt1': 'Njalo nabantu bonke',
  'assessment.quiz_safety_q3_opt2': 'Kunoma yiliphi iwebhusayithi',
  'assessment.quiz_safety_q3_opt3': 'Ngekubhange lakho',
  'loginScreen.subtitle': 'Kunikezwa Amandla Ikusasa Ledijithali',
  'loginScreen.logInTab': 'Ngena',
  'loginScreen.signUpTab': 'Bhalisa',
  'loginScreen.sendOtp': 'Thumela i-OTP',
  'loginScreen.continueBtn': 'Qhubeka',
  'loginScreen.registerWithEmail': 'Bhalisa nge-imeyili',
  'loginScreen.registerWithPhone': 'Bhalisa ngenombolo yefoni',
  'loginScreen.loginWithEmail': 'Ngena nge-imeyili',
  'loginScreen.loginWithPhone': 'Ngena ngenombolo yefoni',
  'loginScreen.or': 'noma',
  'loginScreen.createAccount': 'Dala i-akhawunti',
  'loginScreen.alreadyHaveAccountLogin': 'Usunayo i-akhawunti?',
  'loginScreen.loginLink': 'Ngena',
  'loginScreen.orLoginWith': 'Noma ngena ngo',
  'loginScreen.rememberMe': 'Ngikhumbule',
  'loginScreen.maintenanceTitle': 'Kuyalenziwa',
  'loginScreen.maintenanceMessage': 'Abasebenzi bethu balungiswa njengamanje. Sicela uzame futhi kamuva.',
  'loginScreen.enterValidPhone': 'Sicela ufake inombolo yefoni evumelekile',
  'loginScreen.enterName': 'Sicela ufake igama lakho',
  'loginScreen.minPassword': 'Iphasiwedi kumele ibe nobude obungenani beepheni eziyi-6',
  'loginScreen.failedToSendCode': 'Kwehlulekile ukuthumela ikhodi yokuqinisekisa',
  'loginScreen.phoneAuthFailed': 'Kwehlulekile ukucubungula ukuqinisekisa kwefoni',
  'loginScreen.invalidResponse': 'Iseva ibuyise impendulo engavumelekile.',
  'loginScreen.loginFailedTitle': 'Ukungena kuhlulekile',
  'loginScreen.checkCredentials': 'Sicela uhlole imininingwane yakho bese uzama futhi',
  'loginScreen.accountCreated': 'I-akhawunti idaliwe ngempumelelo!',
  'loginScreen.signupFailedTitle': 'Ukubhalisa kuhlulekile',
  'loginScreen.noToken': 'Iseva ayibuyisanga i-token.',
  'loginScreen.tryAgain': 'Sicela uzame futhi',
}

def esc(v):
    return v.replace("\\", "\\\\").replace("'", "\\'")

def find_section(lines, name, start_from=0):
    start = None
    for i in range(start_from, len(lines)):
        if re.match(rf"^  {name}: \{{", lines[i]):
            start = i
            break
    if start is None:
        raise RuntimeError(f'section {name} not found')
    depth = 0
    for i in range(start, len(lines)):
        depth += lines[i].count('{') - lines[i].count('}')
        if depth == 0 and i > start:
            return start, i
    raise RuntimeError('unbalanced')

def section_keys(lines, s, e):
    keys = set()
    for i in range(s+1, e):
        m = re.match(r"^    ([a-zA-Z0-9_]+): ", lines[i])
        if m:
            keys.add(m.group(1))
    return keys

def process(lang, entries):
    path = f'i18n/locales/{lang}.ts'
    lines = open(path, encoding='utf-8').read().split('\n')

    # 1. auth.dontHaveAccount after resetPassword line
    a_s, a_e = find_section(lines, 'auth')
    if 'dontHaveAccount' not in section_keys(lines, a_s, a_e):
        idx = next(i for i in range(a_s, a_e) if lines[i].strip().startswith('resetPassword:'))
        lines.insert(idx+1, f"    dontHaveAccount: '{esc(entries['auth.dontHaveAccount'])}',")

    # 2. move misplaced assessment keys out of home into assessment
    MOVE = ['previous','nextButton','submitAssessment','submitConfirmBody','quitTitle',
            'quitBody','quit','trueLabel','falseLabel','typeAnswerPlaceholder','noQuestions']
    h_s, h_e = find_section(lines, 'home')
    moved = {}
    keep = []
    for i in range(len(lines)):
        if h_s <= i <= h_e:
            m = re.match(r"^    ([a-zA-Z0-9_]+): ('.*'),$", lines[i])
            if m and m.group(1) in MOVE:
                moved[m.group(1)] = m.group(2)
                continue
        keep.append(lines[i])
    lines = keep

    a_s, a_e = find_section(lines, 'assessment')
    existing = section_keys(lines, a_s, a_e)
    block = []
    for k in MOVE:
        if k not in existing:
            v = moved.get(k) or f"'{esc(entries[f'assessment.{k}'])}'"
            block.append(f"    {k}: {v},")
    for key in entries:
        if key.startswith('assessment.'):
            suffix = key.split('.')[1]
            if suffix not in existing and suffix not in MOVE:
                block.append(f"    {suffix}: '{esc(entries[key])}',")
    if block:
        idx = next(i for i in range(a_s, a_e) if lines[i].strip().startswith('quizInstructions:'))
        lines[idx+1:idx+1] = block

    # 3. loginScreen section before tools
    if 'loginScreen' not in ''.join(l[:20] for l in lines if re.match(r"^  loginScreen", l)):
        t_s, _ = find_section(lines, 'tools')
        ls_block = ['  loginScreen: {']
        for key in entries:
            if key.startswith('loginScreen.'):
                suffix = key.split('.')[1]
                ls_block.append(f"    {suffix}: '{esc(entries[key])}',")
        ls_block.append('  },')
        lines[t_s:t_s] = ls_block

    open(path, 'w', encoding='utf-8').write('\n'.join(lines))
    print(lang, 'updated OK')

process('af', AF)
process('zu', ZU)

# 4. missing auth.dontHaveAccount in the other 8 languages
OTHERS = {
  'xh': 'Unayo na i-akhawunti?',
  'tn': 'A o na le akhaonto?',
  've': 'Ni sa na na akhawunti?',
  'ts': 'Wa ni akaunti?',
  'nso': 'Na le akhaonte?',
  'st': "Na le ak'haonte?",
  'nr': 'Une i-akhawunti na?',
  'ss': 'Unako i-akhawunti?',
}
for lang, val in OTHERS.items():
    path = f'i18n/locales/{lang}.ts'
    lines = open(path, encoding='utf-8').read().split('\n')
    a_s, a_e = find_section(lines, 'auth')
    if 'dontHaveAccount' in section_keys(lines, a_s, a_e):
        print(lang, 'already has key'); continue
    idx = next(i for i in range(a_s, a_e) if lines[i].strip().startswith('resetPassword:'))
    lines.insert(idx+1, f"    dontHaveAccount: '{esc(val)}',")
    open(path, 'w', encoding='utf-8').write('\n'.join(lines))
    print(lang, 'added dontHaveAccount')

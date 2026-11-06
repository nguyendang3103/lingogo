# -*- coding: utf-8 -*-
"""
Công cụ tạo phiên âm chuẩn IPA giọng Mỹ (General American) theo chuẩn từ điển Cambridge/Oxford
cho toàn bộ 640 từ vựng và cụm từ tiếng Anh trong data/en.json.
"""
import os, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

import eng_to_ipa
cmu_path = os.path.join(os.path.dirname(eng_to_ipa.__file__), 'resources', 'CMU_dict.json')
with open(cmu_path, encoding='utf-8') as f:
    cmu = json.load(f)

VOWEL_MAP = {
    'aa': 'ɑː', 'ae': 'æ', 'ah0': 'ə', 'ah1': 'ʌ', 'ah2': 'ʌ',
    'ao': 'ɔː', 'aw': 'aʊ', 'ay': 'aɪ', 'eh': 'e',
    'er0': 'ɚ', 'er1': 'ɝː', 'er2': 'ɝː',
    'ey': 'eɪ', 'ih0': 'ə', 'ih1': 'ɪ', 'ih2': 'ɪ',
    'iy0': 'i', 'iy1': 'iː', 'iy2': 'iː',
    'ow': 'oʊ', 'oy': 'ɔɪ', 'uh': 'ʊ',
    'uw0': 'uː', 'uw1': 'uː', 'uw2': 'uː',
}

CONS_MAP = {
    'b': 'b', 'ch': 'tʃ', 'd': 'd', 'dh': 'ð', 'f': 'f', 'g': 'ɡ',
    'hh': 'h', 'jh': 'dʒ', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n',
    'ng': 'ŋ', 'p': 'p', 'r': 'r', 's': 's', 'sh': 'ʃ', 't': 't',
    'th': 'θ', 'v': 'v', 'w': 'w', 'y': 'j', 'z': 'z', 'zh': 'ʒ'
}

ONSET_CLUSTERS = {
    'pl', 'pr', 'bl', 'br', 'tr', 'dr', 'kl', 'kr', 'gl', 'gr',
    'fl', 'fr', 'th', 'sp', 'st', 'sk', 'sl', 'sm', 'sn', 'sw',
    'spl', 'spr', 'str', 'skr', 'skw'
}

SHORT_VOWELS = {'ae', 'eh', 'ih', 'ah', 'uh'}

SPECIAL_WORDS = {
    'cif': 'ˌsiː.aɪˈef',
    'fob': 'ˌef.oʊˈbiː',
    'exw': 'ˌiː.eksˈdʌb.əl.juː',
    'fca': 'ˌef.siːˈeɪ',
    'fcl': 'ˌef.siːˈel',
    'lcl': 'ˌel.siːˈel',
    'dap': 'ˌdiː.eɪˈpiː',
    'ddp': 'ˌdiː.diːˈpiː',
    'eta': 'ˌiː.tiːˈeɪ',
    'etd': 'ˌiː.tiːˈdiː',
    'moq': 'ˌem.oʊˈkjuː',
    'mto': 'ˌem.tiːˈoʊ',
    'mts': 'ˌem.tiːˈes',
    'sku': 'skjuː',
    'oem': 'ˌoʊ.iːˈem',
    'odm': 'ˌoʊ.diːˈem',
    'nre': 'ˌen.ɑːrˈiː',
    'rfq': 'ˌɑːr.efˈkjuː',
    'rfi': 'ˌɑːr.efˈaɪ',
    'sla': 'ˌes.elˈeɪ',
    'kpi': 'ˌkeɪ.piːˈaɪ',
    'qc': 'ˌkjuːˈsiː',
    'iso': 'ˈaɪ.soʊ',
    'gst': 'ˌdʒiː.esˈtiː',
    'raci': 'ˈreɪ.si',
    'nda': 'ˌen.diːˈeɪ',
    'hs': 'ˌeɪtʃˈes',
    'sdk': 'ˌes.diːˈkeɪ',
    'api': 'ˌeɪ.piːˈaɪ',
    'po': 'ˌpiːˈoʊ',
    'b/l': 'ˌbiːˈel',
    'c/o': 'ˌsiːˈoʊ',
    'co': 'ˌsiːˈoʊ',
    '3pl': 'ˌθriː.piːˈel',
    '4pl': 'ˌfɔːr.piːˈel',
    'third-party': 'ˌθɝːdˈpɑːr.t̬i',
    'fourth-party': 'ˌfɔːrθˈpɑːr.t̬i',
    'demurrage': 'dɪˈmɝː.ɪdʒ',
    'laytime': 'ˈleɪ.taɪm',
    'consignee': 'ˌkɑːn.saɪˈniː',
    'transshipment': 'trænsˈʃɪp.mənt',
    'stockout': 'ˈstɑːk.aʊt',
    'backorder': 'ˈbækˌɔːr.dɚ',
    'palletize': 'ˈpæl.ə.taɪz',
    'volumetric': 'ˌvɑːl.jəˈme.trɪk',
    'ispm': 'ˌaɪ.es.piːˈem',
    'lidar': 'ˈlaɪ.dɑːr',
    'runtime': 'ˈrʌn.taɪm',
    'waypoint': 'ˈweɪˌpɔɪnt',
    'troubleshooting': 'ˈtrʌb.əlˌʃuː.t̬ɪŋ',
    'digitalization': 'ˌdɪdʒ.ə.t̬əl.əˈzeɪ.ʃən',
    'onboarding': 'ˈɑːnˌbɔːr.dɪŋ',
    'shortlist': 'ˈʃɔːrt.lɪst',
    'swappable': 'ˈswɑː.pə.bəl',
    'unboxing': 'ʌnˈbɑːk.sɪŋ',
    'rebrand': 'ˌriːˈbrænd',
    'offtake': 'ˈɔːf.teɪk',
    'nearshore': 'ˈnɪr.ʃɔːr',
    'farshore': 'ˈfɑːr.ʃɔːr',
    'cladding': 'ˈklæd.ɪŋ',
    'compressive': 'kəmˈpres.ɪv',
    'calorific': 'ˌkæl.əˈrɪf.ɪk',
    'biosecurity': 'ˌbaɪ.oʊ.səˈkjʊr.ə.t̬i',
    'tannin': 'ˈtæn.ɪn',
    'sommelier': 'ˌsɑːm.əlˈjeɪ',
    'incoterms': 'ˈɪŋ.koʊ.tɝːmz',
    'un38.3': 'ˌjuːˈen ˌθɝː.t̬iˈeɪt pɔɪnt θriː',
    'un38': 'ˌjuːˈen ˌθɝː.t̬iˈeɪt',
    'iso 9001': 'ˈaɪ.soʊ ˌnaɪnˈθaʊ.zənd wʌn',
    '9001': 'ˌnaɪnˈθaʊ.zənd wʌn',
    '15': 'ˌfɪfˈtiːn',
    '3': 'θriː',
    'scor': 'skɔːr',
    'lead': 'liːd',
    'to': 'tuː',
    'of': 'əv',
    'a': 'ə',
    'in': 'ɪn',
    'for': 'fɚ',
    'and': 'ænd',
    'be': 'biː',
    'the': 'ðiː'
}

def is_vowel(p):
    return any(p.startswith(v) for v in ['aa', 'ae', 'ah', 'ao', 'aw', 'ay', 'eh', 'er', 'ey', 'ih', 'iy', 'ow', 'oy', 'uh', 'uw'])

def syllabify(phones):
    v_indices = [i for i, p in enumerate(phones) if is_vowel(p)]
    if not v_indices:
        return [(phones, '0')]
    
    sylls = []
    for i, v_idx in enumerate(v_indices):
        v = phones[v_idx]
        if i == 0:
            onset_start = 0
        else:
            prev_v = phones[v_indices[i-1]]
            prev_base = prev_v[:2]
            prev_stress = prev_v[-1] if prev_v[-1] in '012' else '0'
            inter = phones[v_indices[i-1]+1 : v_idx]
            
            if len(inter) == 0:
                onset_start = v_idx
            elif len(inter) == 1:
                if prev_base in SHORT_VOWELS and prev_stress in ('1', '2'):
                    onset_start = v_idx
                else:
                    onset_start = v_idx - 1
            elif len(inter) == 2:
                pair = inter[0] + inter[1]
                if prev_base in SHORT_VOWELS and prev_stress in ('1', '2'):
                    onset_start = v_idx - 1
                elif pair in ONSET_CLUSTERS:
                    onset_start = v_idx - 2
                else:
                    onset_start = v_idx - 1
            else:
                onset_start = v_idx - 1
                
        sylls.append({
            'start': onset_start,
            'v_idx': v_idx,
            'stress': v[-1] if v[-1] in '012' else '0'
        })
        
    res = []
    for i in range(len(sylls)):
        st = sylls[i]['start']
        end = sylls[i+1]['start'] if i+1 < len(sylls) else len(phones)
        res.append((phones[st:end], sylls[i]['stress']))
    return res

def convert_syll(phones, stress, is_first, is_last):
    out = []
    for j, p in enumerate(phones):
        if is_vowel(p):
            base = p[:2]
            key = p if p in VOWEL_MAP else base
            if p == 'ih0' and is_first and j == 0:
                ipa_v = 'ɪ'
            elif p == 'ih0' and is_last and j < len(phones)-1 and phones[j+1] == 'ng':
                ipa_v = 'ɪ'
            else:
                ipa_v = VOWEL_MAP.get(key, VOWEL_MAP.get(base, base))
            out.append(ipa_v)
        else:
            out.append(CONS_MAP.get(p, p))
    s = ''.join(out)
    if stress == '1':
        return 'ˈ' + s
    elif stress == '2':
        return 'ˌ' + s
    return s

def single_word_to_ipa(w):
    clean = w.lower().strip("',.!?()")
    if not clean:
        return ''
    if clean in SPECIAL_WORDS:
        return SPECIAL_WORDS[clean]
    if clean not in cmu:
        return clean
    candidates = cmu[clean]
    cand = candidates[0]
    if clean == 'schedule' and len(candidates) > 1:
        for c in candidates:
            if 'uw' in c:
                cand = c; break
    elif clean == 'production' and len(candidates) > 1:
        for c in candidates:
            if c.startswith('p r ah0'):
                cand = c; break

    phones = cand.split()
    sylls = syllabify(phones)
    converted_sylls = [convert_syll(ph, st, i == 0, i == len(sylls)-1) for i, (ph, st) in enumerate(sylls)]
    
    res = ''
    for i, s in enumerate(converted_sylls):
        if i == 0:
            res += s
        else:
            if s.startswith('ˈ') or s.startswith('ˌ'):
                res += s
            else:
                res += '.' + s
    return res

def token_to_ipa(tok):
    clean = tok.lower().strip()
    if clean in SPECIAL_WORDS:
        return SPECIAL_WORDS[clean]
    if '-' in tok:
        parts = tok.split('-')
        return '-'.join(token_to_ipa(p) for p in parts)
    if '/' in tok:
        parts = tok.split('/')
        return ' / '.join(token_to_ipa(p) for p in parts)
    if '(' in tok and ')' in tok:
        m = re.match(r'^(.*?)\s*\((.*?)\)$', tok)
        if m:
            main_part = token_to_ipa(m.group(1))
            paren_part = token_to_ipa(m.group(2))
            return f"{main_part} ({paren_part})"
    return single_word_to_ipa(tok)

def phrase_to_ipa(phrase):
    p_clean = phrase.strip()
    m_paren = re.match(r'^(.*?)\s*\((.*?)\)$', p_clean)
    if m_paren:
        main_text = m_paren.group(1).strip()
        paren_text = m_paren.group(2).strip()
        main_ipa = phrase_to_ipa_core(main_text)
        paren_ipa = phrase_to_ipa_core(paren_text)
        return f"/{main_ipa} ({paren_ipa})/"
    
    if ' / ' in p_clean:
        parts = p_clean.split(' / ')
        ipas = [phrase_to_ipa_core(p) for p in parts]
        return f"/{' / '.join(ipas)}/"
    
    return f"/{phrase_to_ipa_core(p_clean)}/"

def phrase_to_ipa_core(text):
    words = text.split()
    ipas = []
    for w in words:
        if '-' in w and w.lower() not in SPECIAL_WORDS:
            subwords = w.split('-')
            sub_ipas = [token_to_ipa(sw) for sw in subwords]
            ipas.append('-'.join(sub_ipas))
        else:
            ipas.append(token_to_ipa(w))
    return ' '.join(ipas)

def main():
    with open('data/en.json', 'r', encoding='utf-8') as f:
        en = json.load(f)

    count = 0
    for t in en.get('topics', []):
        for v in t.get('vocab', []):
            v['r'] = phrase_to_ipa(v['w'])
            count += 1

    with open('data/en.json', 'w', encoding='utf-8') as f:
        json.dump(en, f, ensure_ascii=False, separators=(',', ':'))

    print(f"Cập nhật thành công {count} từ vựng trong data/en.json")
    print("production schedule ->", phrase_to_ipa('production schedule'))

if __name__ == '__main__':
    main()

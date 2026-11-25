import re
import sys

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    target_block = """                // Sub-card F: 🏛️ एस्ट्रो-वास्तु एवं लाल किताब सोए भाव जागृति
                var sleepingHouseText = 'यदि १०वां भाव खाली हो तो २रा सोया रहता है, और २रा खाली हो तो ९वां व १०वां सोया रहता है। १०वें भाव को जगाने हेतु सरकारी भवन के कोने में सौंफ रखें; २रे/४थे भाव हेतु ४३ दिन चावल व तांबा सिक्का धर्मस्थान में अर्पित करें।';
                var astroVastuText = 'उत्तर-पश्चिम (शुक्र दिशा) में गुलाब/सुगंध स्थापित करें; घर में टूटा शीशा या नल से पानी टपकना (लीकेज) तुरंत बंद करें; पश्चिम दिशा से तीखी धूप आने पर पर्दे लगाएं।';

                h += '<div style="background:rgba(15,23,42,0.7); border:1px solid rgba(244,114,182,0.3); border-radius:8px; padding:12px 14px;">';
                h += '<div style="display:flex; align-items:center; gap:6px; margin-bottom:8px;">';
                h += '<span style="color:#f472b6; font-size:1rem;">🏛️</span>';
                h += '<b style="color:#f472b6; font-size:0.88rem;">एस्ट्रो-वास्तु, नक्षत्र पूजा एवं सोए भाव जागृति</b>';
                h += '</div>';
                h += '<div style="font-size:0.75rem; color:#94a3b8; margin-bottom:8px;">४३-दिवसीय ऊर्जा संतुलन, वास्तु पूर्व-लक्षण एवं नक्षत्र संरेखण:</div>';
                h += '<ul style="margin:0; padding-left:16px; font-size:0.84rem; line-height:1.65; color:var(--text-secondary);">';
                h += '<li style="margin-bottom:6px;"><b>सोए भाव जागृति:</b> ' + sleepingHouseText + '</li>';
                h += '<li style="margin-bottom:6px;"><b>एस्ट्रो-वास्तु व २७ नक्षत्र:</b> ' + astroVastuText + ' (हस्त नक्षत्र में दान १५ दिन में फल देता है; रेवती में क्षमा-प्रार्थना)।</li>';
                h += '</ul></div>';"""

    replacement_block = """                // Sub-card F: 🏛️ एस्ट्रो-वास्तु एवं लाल किताब सोए भाव जागृति
                var sleepingHouseText = 'यदि १०वां भाव खाली हो तो २रा सोया रहता है, और २रा खाली हो तो ९वां व १०वां सोया रहता है। १०वें भाव को जगाने हेतु सरकारी भवन के कोने में सौंफ रखें; २रे/४थे भाव हेतु ४३ दिन चावल व तांबा सिक्का धर्मस्थान में अर्पित करें।';
                var astroVastuText = 'उत्तर-पश्चिम (शुक्र दिशा) में गुलाब/सुगंध स्थापित करें; घर में टूटा शीशा या नल से पानी टपकना (लीकेज) तुरंत बंद करें; पश्चिम दिशा से तीखी धूप आने पर पर्दे लगाएं।';

                h += '<div style="background:rgba(15,23,42,0.7); border:1px solid rgba(244,114,182,0.3); border-radius:8px; padding:12px 14px;">';
                h += '<div style="display:flex; align-items:center; gap:6px; margin-bottom:8px;">';
                h += '<span style="color:#f472b6; font-size:1rem;">🏛️</span>';
                h += '<b style="color:#f472b6; font-size:0.88rem;">एस्ट्रो-वास्तु, नक्षत्र पूजा एवं सोए भाव जागृति</b>';
                h += '</div>';
                h += '<div style="font-size:0.75rem; color:#94a3b8; margin-bottom:8px;">४३-दिवसीय ऊर्जा संतुलन, वास्तु पूर्व-लक्षण एवं नक्षत्र संरेखण:</div>';
                h += '<ul style="margin:0; padding-left:16px; font-size:0.84rem; line-height:1.65; color:var(--text-secondary);">';
                h += '<li style="margin-bottom:6px;"><b>सोए भाव जागृति:</b> ' + sleepingHouseText + '</li>';
                h += '<li style="margin-bottom:6px;"><b>एस्ट्रो-वास्तु व २७ नक्षत्र:</b> ' + astroVastuText + ' (हस्त नक्षत्र में दान १५ दिन में फल देता है; रेवती में क्षमा-प्रार्थना)।</li>';
                h += '</ul></div>';

                // Sub-card G: 🔲 तांत्रिक एवं वैदिक अंकीय नवग्रह यंत्र ग्रिड (3x3 Magic Square)
                var yantraGrids = {
                    'सूर्य': { sum: 15, grid: [[6,1,8],[7,5,3],[2,9,4]], metal: 'तांबा / स्वर्ण', ink: 'केसर-लाल चंदन', dir: 'पूर्व', beej: 'ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः' },
                    'चन्द्र': { sum: 18, grid: [[7,2,9],[8,6,4],[3,10,5]], metal: 'चांदी', ink: 'श्वेत चंदन', dir: 'वायव्य (NW)', beej: 'ॐ श्रां श्रीं श्रौं सः चंद्रमसे नमः' },
                    'मंगल': { sum: 21, grid: [[8,3,10],[9,7,5],[4,11,6]], metal: 'तांबा', ink: 'लाल चंदन-रोली', dir: 'दक्षिण', beej: 'ॐ क्रां क्रीं क्रौं सः भौमाय नमः' },
                    'बुध': { sum: 24, grid: [[9,4,11],[10,8,6],[5,12,7]], metal: 'कांसा / भोजपत्र', ink: 'अष्टगंध', dir: 'उत्तर', beej: 'ॐ ब्रां ब्रीं ब्रौं सः बुधाय नमः' },
                    'गुरु': { sum: 27, grid: [[10,5,12],[11,9,7],[6,13,8]], metal: 'पीतल / स्वर्ण', ink: 'हल्दी-केसर', dir: 'ईशान (NE)', beej: 'ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः' },
                    'शुक्र': { sum: 30, grid: [[11,6,13],[12,10,8],[7,14,9]], metal: 'चांदी / स्फटिक', ink: 'श्वेत चंदन-इत्र', dir: 'आग्नेय (SE)', beej: 'ॐ द्रां द्रीं द्रौं सः शुक्राय नमः' },
                    'शनि': { sum: 33, grid: [[12,7,14],[13,11,9],[8,15,10]], metal: 'लोहा / अष्टधातु', ink: 'काजल-तिल तेल', dir: 'पश्चिम', beej: 'ॐ प्रां प्रीं प्रौं सः शनैश्चराय नमः' },
                    'राहु': { sum: 36, grid: [[13,8,15],[14,12,10],[9,16,11]], metal: 'तांबा / सीसा', ink: 'अष्टगंध', dir: 'नैऋत्य (SW)', beej: 'ॐ भ्रां भ्रीं भ्रौं सः राहवे नमः' },
                    'केतु': { sum: 39, grid: [[14,9,16],[15,13,11],[10,17,12]], metal: 'तांबा / भोजपत्र', ink: 'अष्टगंध', dir: 'ईशान-नैऋत्य', beej: 'ॐ स्रां स्रीं स्रौं सः केतवे नमः' }
                };

                var targetGraha = lagnaLord || 'सूर्य';
                if (!yantraGrids[targetGraha]) targetGraha = 'सूर्य';
                var yData = yantraGrids[targetGraha];

                h += '<div style="background:rgba(15,23,42,0.7); border:1px solid rgba(212,175,55,0.3); border-radius:8px; padding:12px 14px;">';
                h += '<div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">';
                h += '<div style="display:flex; align-items:center; gap:6px;">';
                h += '<span style="color:#fde047; font-size:1rem;">🔲</span>';
                h += '<b style="color:#fde047; font-size:0.88rem;">सिद्ध अंकीय नवग्रह यंत्र ग्रिड (३×३ अंक-चक्र: योग ' + yData.sum + ')</b>';
                h += '</div>';
                h += '<span style="font-size:0.70rem; color:#94a3b8; background:rgba(212,175,55,0.12); padding:2px 6px; border-radius:4px;">' + targetGraha + ' यंत्र</span>';
                h += '</div>';
                h += '<div style="display:flex; flex-wrap:wrap; gap:12px; align-items:center; margin-bottom:8px;">';
                h += '<div style="display:inline-block; border:2px solid #d4af37; border-radius:6px; overflow:hidden; background:rgba(0,0,0,0.5);">';
                h += '<table style="border-collapse:collapse; text-align:center; font-weight:700; font-size:0.85rem; color:#fde047;">';
                for (var r = 0; r < 3; r++) {
                    h += '<tr>';
                    for (var c = 0; c < 3; c++) {
                        h += '<td style="border:1px solid rgba(212,175,55,0.4); padding:4px 9px; min-width:28px;">' + yData.grid[r][c] + '</td>';
                    }
                    h += '</tr>';
                }
                h += '</table></div>';
                h += '<div style="flex:1; min-width:180px; font-size:0.78rem; color:var(--text-secondary); line-height:1.55;">';
                h += '<div><b>धातु/माध्यम:</b> ' + yData.metal + ' (भोजपत्र पर अनार कलम श्रेष्ठ)</div>';
                h += '<div><b>स्याही:</b> ' + yData.ink + ' | <b>दिशा:</b> ' + yData.dir + '</div>';
                h += '<div><b>प्राण-प्रतिष्ठा मंत्र (१०८ बार):</b> <code style="color:#fde047; font-size:0.75rem;">' + yData.beej + '</code></div>';
                h += '</div></div>';
                h += '<div style="font-size:0.73rem; color:#94a3b8; font-style:italic;">* यंत्र बिना किसी दुष्प्रभाव के संबंधित ग्रह की प्राण-ऊर्जा को संतुलित व आकर्षित करने का अचूक माध्यम है।</div>';
                h += '</div>';

                // Sub-card H: 🌿 सार्वभौमिक चतुर्-आचरण नियम एवं पारिवारिक ग्रह-शांति
                h += '<div style="background:rgba(15,23,42,0.7); border:1px solid rgba(16,185,129,0.3); border-radius:8px; padding:12px 14px;">';
                h += '<div style="display:flex; align-items:center; gap:6px; margin-bottom:8px;">';
                h += '<span style="color:#10b981; font-size:1rem;">🌿</span>';
                h += '<b style="color:#10b981; font-size:0.88rem;">सार्वभौमिक चतुर्-आचरण नियम एवं पारिवारिक ग्रह-संतुलन</b>';
                h += '</div>';
                h += '<div style="font-size:0.75rem; color:#94a3b8; margin-bottom:8px;">सर्व-दोष नाशक चार दिव्य आचरण एवं पारिवारिक संबंधों से निःशुल्क ग्रह-शांति:</div>';
                h += '<ul style="margin:0; padding-left:16px; font-size:0.83rem; line-height:1.6; color:var(--text-secondary);">';
                h += '<li style="margin-bottom:5px;"><b>४-आचरण नियम:</b> (१) पुराणों/धर्मग्रंथों का नित्य श्रवण, (२) पंचमेश इष्टदेव का ध्यान, (३) किसी भी जीव/पादप को अकारण कष्ट न देना (अहिंसा), (४) जीवनसाथी के प्रति पूर्ण निष्ठा। यह चार आचरण मारक दशा, कालसर्प व साढ़ेसाती का अशुभ प्रभाव समाप्त कर देते हैं।</li>';
                h += '<li style="margin-bottom:5px;"><b>पारिवारिक ग्रह-संतुलन:</b> पिता/पितामह आदर (सूर्य), माता सेवा (चंद्र), भ्राता स्नेह (मंगल), बहन/बेटी/कन्या सत्कार (बुध), गुरु वंदना (गुरु), जीवनसाथी सम्मान (शुक्र), वृद्धजन व सेवक स्नेह (शनि), ससुराल पक्ष निष्कपटता (राहु), पुत्र व श्वान सेवा (केतु)।</li>';
                h += '</ul></div>';"""

    if target_block not in content:
        print(f"Error: Target block not found in {filepath}!")
        return False

    new_content = content.replace(target_block, replacement_block, 1)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully patched {filepath}!")
    return True

if __name__ == '__main__':
    ok1 = patch_file('js/vyas_daivagya_engine.js')
    ok2 = patch_file('android_app/app/src/main/assets/js/vyas_daivagya_engine.js')
    if ok1 and ok2:
        print("All files patched successfully.")
    else:
        sys.exit(1)


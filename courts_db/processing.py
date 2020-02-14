# # import json
# #
# # with open('data/courts.json', "r") as f:
# #     court_data = json.loads(f.read())
# #
# #
# # for court in court_data['courts']:
# #     print court['name'].strip(), '\t',
# #     for date in court['dates']:
# #         print date['start'], '\t', date['end'], "\t\t",
# #
# #     print ""
#
# # for court in court_data['courts']:
# #     if "examples" in court.keys():
# #         pass
# #     else:
# #         court['examples'] = []
#
# # with open('data.txt', "r") as f:
# #     temp = json.loads(f.read())
#
#
# # # print temp
# #
# # for court in court_data['courts']:
# #     if court['id'] is not None:
# #         if court['id'] in temp.keys():
# #             # print temp[court['id']]
# #
# #             if court['name'] == "":
# #                 # print temp[court['id']]['full_name'].strip()
# #                 court['name'] = temp[court['id']]['full_name'].strip()
# #             if court['dates'][0]['start'] is None and len(court['dates']) == 1:
# #                 if temp[court['id']]['start_date'] != "None":
# #                     # print temp[court['id']]['start_date']
# #                     court['dates'][0]['start'] = temp[court['id']]['start_date']
# #
# #                 if temp[court['id']]['end_date'] != "None":
# #                     # print temp[court['id']]['end_date']
# #                     court['dates'][0]['end'] = temp[court['id']]['end_date']
# #
# #             if temp[court['id']]['jurisdiction'][0] == "F":
# #                 # print "FEDERAL"
# #                 court['system'] = "Federal"
# #             if temp[court['id']]['jurisdiction'][0] == "S":
# #                 # print "State"
# #                 court['system'] = "State"
# #             # if temp[court['id']]['jurisdiction'][1] == "A":
# #             #     print "Appellate"
# #             if temp[court['id']]['url'] != "":
# #                 court['court_url'] = temp[court['id']]['url']
# # #
# # with open("examples_court.json", "w") as write_file:
# #     json.dump(court_data, write_file, indent=4)
#
# # from bs4 import BeautifulSoup as bs4
# #
# # with open("lexis2.html", "r") as f:
# #     r = f.read()
# #
# # soup = bs4(r, "html.parser")
# # for btn in soup.find_all("button", {"class":"filtertree-expander"}):
# #     print btn
# #
# # for input in soup.find_all("span", {"class":"filterval-text"}):
# #     print input.text, "\t", input.findNext('span', {"class":"filterval-count"}).text
#
import re
#
# # court_str = "248.	Washington Municipal Court, Fife"
sregex = re.compile(r"\b(/AL|Alabama|AK|Alaska|AZ|Arizona|AR|Arkansas|CA|California|CO|Colorado|CT|Connecticut|DE|Delaware|FL|Florida|GA|Georgia|HI|Hawaii|ID|Idaho|IL|Illinois|IN|Indiana|IA|Iowa|KS|Kansas|KY|Kentucky|LA|Louisiana|ME|Maine|MD|Maryland|MA|Massachusetts|MI|Michigan|MN|Minnesota|MS|Mississippi|MO|Missouri|MT|Montana|NE|Nebraska|NV|Nevada|NH|New Hampshire|NJ|New Jersey|NM|New Mexico|NY|New York|NC|North Carolina|ND|North Dakota|OH|Ohio|OK|Oklahoma|OR|Oregon|PA|Pennsylvania|RI|Rhode Island|SC|South Carolina|SD|South Dakota|TN|Tennessee|TX|Texas|UT|Utah|VT|Vermont|VA|Virginia|WA|Washington|WV|West Virginia|WI|Wisconsin|WY|Wyoming/)\b")
# regex = re.compile(r"[0-9]{1,5}\W{1,3}\W(.*),(.*)", re.I)
# # print re.search(regex, court_str).group(2)
# #
# # print re.search(states, 'Alabama Probate Court  St. Clair County').group()
# with open("allcourts.txt", "r") as f:
#     r = f.read().splitlines()
# xxx = []
# cd = []
# for item in r:
#     if "." in item:
#         f = re.search(regex, item)
#         if not f:
#             if re.search(states, item):
#                 state = re.search(states, item).group()
#                 middle = item.split(re.search(states, item).group())[1]
#                 sub = ""
#                 start = ""
#                 end = ""
#                 if "Justice of the Peace Court" in middle:
#                     sub = middle.split("Justice of the Peace Court")[1]
#                     middle = "Justice of the Peace Court"
#                 if " - " in middle:
#                     sub = middle.split(" - ")[1]
#                     middle = middle.split("-")[0]
#                 if "District Court of Appeal" in middle:
#                     sub = middle.replace(" Court of Appeal", "")
#                     middle = middle.replace(sub, "")
#                 if "(" in middle:
#                     dates = middle.split(" (")[1]
#                     start = dates[:4]
#                     end = dates[5:-1]
#                     middle = middle.split(" (")[0]
#                 print state.strip(), "\t\t", middle,"\t\t", sub, start, end, "\t\t", item
#                 cd.append({
#                             "state":state.strip(),
#                            "court":middle.strip(),
#                            "sub":sub.strip(),
#                            # "location":location.strip(),
#                             "start":start,
#                             "end":end,
#                             "name":item.split(".", 1)[1].strip()
#                            })
#                 # print re.search(states, item).group(), "\t", item.split(re.search(states, item).group())[1], "\t\t\t", item
#         #     # print f.groups()
#         #     # print f.group(1)
#         #     x = re.search(states, f.group(1))
#         #     if x:
#         #         # print  x.group(), "\t-\t", f.group(1).replace(x.group(), "").split(","),"\t-\t", f.group(2)
#         #         state = x.group()
#         #         middle = f.group(1).replace(x.group(), "").split(",")
#         #         court = middle[0]
#         #         location = f.group(2)
#         #         sub_court = ""
#         #         if len(middle) > 1:
#         #             sub_court = middle[1]
#         #
#         #             if "County" in sub_court:
#         #                 location = sub_court
#         #                 sub_court = f.group(2)
#         #
#         #
#         # cd.append({
#         #             "state":state.strip(),
#         #            "court":court.strip(),
#         #            "sub":sub_court.strip(),
#         #            "location":location.strip()
#         #            }
#         # )
#         # print state, court, sub_court, location
#
# # import json
# # with open('all_crts3.json', 'w') as f:
# #     json.dump(cd, f, indent=4)
#
#
#     # print item
# # for item in r:
# #     try:
# #         print item
# #         xxx.append(item.split(".")[1].split(",")[0].strip())
# #     except:
# #         pass
# #
# # xyx = list(set(xxx))
# # print len(xyx)
# # for item in sorted(xyx):
# #     print item

def sort_by_location(d):
    '''a helper function for sorting'''
    if d['location'] != "":
        return d['location']
    return "zzz"
#
import json
import re
# #
with open('circuit_created.json', "r") as f:
    all_courts = json.loads(f.read())
# cd = []
# for court in all_courts:
#     if court['state'] == "Arizona":
#         print court
#         cd.append(court['location'])
#
# for c in sorted(list(set(cd))):
#     print c

sorted_json = sorted(all_courts, key=sort_by_location)

with open("sorted_circut.json", "w") as write_file:
    json.dump(sorted_json, write_file, indent=4)

# templateX = {
#         "regex": [],
#         "name_abbreviation": "",
#         "dates": [
#             {
#                 "start": "",
#                 "end": ""
#             }
#         ],
#         "name": "",
#         "level": "iac",
#         "case_types": [],
#         "system": "federal",
#         "examples": [
#         ],
#         "type": "appellate",
#         "id": "circt",
#         "location": ""
#     }
# with open('cirtcuits.txt', "r") as f:
#     circuits = f.read().splitlines()
#
# cd = []
# import pprint
# for circuit in circuits:
#     template = templateX
#     if "." in circuit and 'Cts' not in circuit:
#         court, start, stop = circuit.strip().split("(")[0].strip(), \
#             circuit.strip().split("(")[1].split("-")[0].strip(), \
#             circuit.strip().split("(")[1].split("-")[1].split(")")[0]
#         na = "%s Cir. Ct" % court
#         name = "U.S. Circuit Court for the District of %s" % court
#         regex = "Circuit Court %s" % court[:-1].replace(". ", " D ")
#
#         id = "circt" + "".join([x.strip(".") for x in court.lower().split(" ")])
#         sd = "%s-01-01" % start
#         ed = "%s-12-31" % stop
#         template['name'] = name
#         template['name_abbreviation'] = na
#         template['dates'][0]['start'] = sd
#         template['dates'][0]['end'] = ed
#         template['regex'] = regex
#         template['location'] = regex.split(" ")[-1]
#         template['id'] = id.replace("distofcolumbia", "dc").replace("massachusetts", "mass").replace(".", "")
#         abc = template
#
#         pp = pprint.PrettyPrinter(indent=4)
#         pp.pprint(template)
#         print ","
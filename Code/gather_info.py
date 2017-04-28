from bs4 import BeautifulSoup
import requests
import re
import os
import csv

##### ORI analysis #######
webpage = "https://ori.hhs.gov/case_summary"
# Download to cases.html
os.system("wget " + webpage + " -O ../Data/cases.html")
soup = BeautifulSoup(open("cases.html"), "lxml")
cases_links = [x.get('href') for x in soup.find_all(
    'a') if re.search("/content/case", str(x)) is not None]

# Download the page of each link
webpage = "https://ori.hhs.gov/"
for case in cases_links:
    name = re.match(".*case-summary-([\w-]+)", case).groups()[0]
    os.system("wget " + webpage + case +
              " -O ../Data/files_ori_cases/" + name + ".html")

# extract statements
Dir = "../Data/files_ori_cases/"
F = [os.path.abspath(os.path.join(dirpath, f))
     for dirpath, _, filenames in os.walk(Dir) for f in filenames]

# one of the webpages(Poehlman, Eric T.) was replaced manually since the
# structure was different
Statements = {x: BeautifulSoup(open(x), "lxml").find(
    'div', attrs={'class': "field-item even"}).get_text() for x in F}

# parse statements
# one case (Kornak, Paul H.) was excluded from the analysis since the case
# was related to negligent homicide of a test subject

pattern_list = [".*(fabricated|fabricati[ong]+|fak[eing]+)[^\.]*(data|report[s]?).*",
                ".*(falsifying|falsified|falsification|false|biasing|manipulat[ioned]+)[^\.]*(data|report[s]?).*",
                ".*(fabricated|fabricati[ong]+|fak[eing]+)[^\.]*(figure[s]?|image[s]?).*",
                ".*(falsifying|falsified|falsification|false|biasing|manipulat[ioned]+)[^\.]*(figure[s]?|image[s]?).*"]

pattern_name = ["fabricated data", "falsified data",
                "fabricated image", "falsified image"]

T = [" ".join([pattern_name[c] for c in range(len(pattern_list)) if re.match(
    pattern_list[c], Statements[x]) is not None]) for x in Statements.keys()]

year = [str(x) for x in range(2000, 2017)]
Y = [[int(x) for x in year if re.match(".*" + x + ".*", Statements[key])
      is not None] for key in Statements.keys()]
# done like this because one of the cases(Reddy Venkata) didn't have a
# year in the statement!!!!
Y = [max(x) if len(x) > 0 else 2015 for x in Y]

# write to file
with open('../Data/data_ori.csv', 'w', newline='') as cases:
    a = csv.writer(cases, delimiter=',')
    a.writerow(["file", "reason", "year"])
    data = [[F[i], T[i], Y[i]] for i in range(len(T))]
    a.writerows(data)

################## Retraction Watch analysis #############################
webpage = "http://retractionwatch.com/"
# Download to rw.html
os.system("wget " + webpage + " -O rw.html")
soup = BeautifulSoup(open("rw.html"), "lxml")

S = [yy.text.replace('\xa0', ' ').strip() for yy in BeautifulSoup([xx for xx in re.split(
    r'<option class="level-0".+?</option>', str(soup.find_all("select")[1]), re.DOTALL)][10]).find_all("option")]

W = [re.match(r'([\w\s\/]+)\s+\(([\d,]+).*', s).groups() for s in S]
W = [[w.strip() for w in x] for x in W]

# write to file
with open('../Data/retraction_watch.csv', 'w', newline='') as rw:
    a = csv.writer(rw, delimiter=',')
    a.writerow(["field", "n_retractions"])
    data = W
    a.writerows(data)

# Give the area number of a.csv SSN as an int and this function returns the location for the area number, abbreviations
# for states and full descriptors for certain special cases. Uses a.csv list of ranges as keys in a.csv dict and then runs
# through the list, generating a.csv string for the possibilities. If more than one region, is it printed as R1,R2 with no
# space inbetween.
# DID

# TODO: In the database resulting from death_master_file_to_db, some states in 251 were categorized as NotIssued, same for 519 (SC and ID respectively)
def determine_state_from_area(area):
    returner = ""
    area_code_dict = {
        range(1, 4): "NH",
        range(4, 8): "ME",
        range(8, 10): "VT",
        range(10, 35): "MA",
        range(35, 40): "RI",
        range(40, 50): "CT",
        range(50, 135): "NY",
        range(135, 159): "NJ",
        range(159, 212): "PA",
        range(212, 221): "MD",
        range(221, 223): "DE",
        range(223, 232): "VA",
        range(691, 700): "VA",
        range(232, 237): "WV",
        range(232, 233): "NC",
        range(237, 247): "NC",
        range(681, 691): "NC",
        range(247, 251): "SC",
        range(654, 659): "SC",
        range(252, 261): "GA",
        range(667, 676): "GA",
        range(261, 268): "FL",
        range(589, 596): "FL",
        range(766, 773): "FL",
        range(268, 303): "OH",
        range(303, 318): "IN",
        range(318, 362): "IL",
        range(362, 387): "MI",
        range(387, 400): "WI",
        range(400, 408): "KY",
        range(408, 416): "TN",
        range(756, 764): "TN",
        range(416, 425): "AL",
        range(425, 429): "MS",
        range(587, 589): "MS",
        range(752, 756): "MS",
        range(429, 433): "AR",
        range(676, 680): "AR",
        range(433, 440): "LA",
        range(659, 666): "LA",
        range(440, 449): "OK",
        range(449, 468): "TX",
        range(627, 646): "TX",
        range(468, 478): "MN",
        range(478, 486): "IA",
        range(486, 501): "MO",
        range(501, 503): "ND",
        range(503, 505): "SD",
        range(505, 509): "NE",
        range(509, 516): "KS",
        range(516, 518): "MT",
        range(518, 519): "ID",
        range(520, 521): "WY",
        range(521, 525): "CO",
        range(650, 654): "CO",
        range(525, 526): "NM",
        range(585, 586): "NM",
        range(648, 650): "NM",
        range(526, 528): "AZ",
        range(600, 602): "AZ",
        range(764, 766): "AZ",
        range(528, 530): "UT",
        range(646, 648): "UT",
        range(530, 531): "NV",
        range(680, 681): "NV",
        range(531, 540): "WA",
        range(540, 545): "OR",
        range(545, 574): "CA",
        range(602, 627): "CA",
        range(574, 575): "AK",
        range(575, 577): "HI",
        range(750, 752): "HI",

        # Special cases
        range(577, 580): "DC",
        range(580, 581): "VI",
        range(580, 585): "c",
        range(596, 600): "PR",
        range(586, 587): "GU,PI,AS",
        range(700, 729): "RailroadBoard",
        range(729, 734): "EnumerationatEntry",
    }
    for key in area_code_dict:
        if area in key:
            returner += area_code_dict[key] + ","
    if returner == "":
        returner = "NotIssued,"
    return returner[:-1]
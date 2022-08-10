# Give the area number of a SSN as an int and this function returns the location for the area number, abbreviations
# for states and full descriptors for certain special cases.

# TODO: 232, 580, and 586 are all shared area numbers, I will have to research when these area numbers shifted.

def determine_state_from_area(area):
    if 1 <= area <= 3:
        return "NH"
    elif 4 <= area <= 7:
        return "ME"
    elif 8 <= area <= 9:
        return "VT"
    elif 10 <= area <= 34:
        return "MA"
    elif 35 <= area <= 39:
        return "RI"
    elif 40 <= area <= 49:
        return "CT"
    elif 50 <= area <= 134:
        return "NY"
    elif 135 <= area <= 158:
        return "NJ"
    elif 159 <= area <= 211:
        return "PA"
    elif 212 <= area <= 220:
        return "MD"
    elif 221 <= area <= 222:
        return "DE"
    elif 223 <= area <= 231:
        return "VA"
    elif 232 == area:
        return "NC"
    # NOTE 232 was also temporarily used
    # for West Virgina
    elif 233 <= area <= 236:
        return "WV"
    elif 247 <= area <= 251:
        return "SC"
    elif 252 <= area <= 260:
        return "GA"
    elif 261 <= area <= 267:
        return "FL"
    elif 268 <= area <= 302:
        return "OH"
    elif 303 <= area <= 317:
        return "IN"
    elif 318 <= area <= 361:
        return "IL"
    elif 362 <= area <= 386:
        return "MI"
    elif 387 <= area <= 399:
        return "WI"
    elif 400 <= area <= 407:
        return "KY"
    elif 408 <= area <= 415:
        return "TN"
    elif 416 <= area <= 424:
        return "AL"
    elif 425 <= area <= 428:
        return "MS"
    elif 429 <= area <= 432:
        return "AR"
    elif 433 <= area <= 439:
        return "LA"
    elif 440 <= area <= 448:
        return "OK"
    elif 449 <= area <= 467:
        return "TX"
    elif 468 <= area <= 477:
        return "MN"
    elif 478 <= area <= 485:
        return "IO"
    elif 486 <= area <= 500:
        return "MO"
    elif 501 <= area <= 502:
        return "ND"
    elif 503 <= area <= 504:
        return "SD"
    elif 505 <= area <= 508:
        return "NE"
    elif 509 <= area <= 515:
        return "KS"
    elif 516 <= area <= 517:
        return "MT"
    elif 518 <= area <= 519:
        return "IO"
    elif 520 == area:
        return "WY"
    elif 521 <= area <= 524:
        return "CO"
    elif 525 == area or area == 585:
        return "NM"
    elif 526 <= area <= 527:
        return "AZ"
    elif 528 <= area <= 529:
        return "UT"
    elif 530 == area or area == 680:
        return "NV"
    elif 531 <= area <= 539:
        return "WA"
    elif 574 == area:
        return "AK"
    elif 540 <= area <= 544:
        return "OR"
    elif 545 <= area <= 573:
        return "CA"
    elif 575 <= area <= 576:
        return "HI"
    elif 577 <= area <= 579:
        return "DC"
    elif 580 == area:
        return "VI"
    # Virgin Islands and Puerto Rico
    # share 580.
    elif 581 <= area <= 584:
        return "PR"
    # 586 is shared by Guam, American
    # Samoa, and the Philippine Islands
    elif 586 == area:
        return "GU/AS/PI"
    elif 700 <= area <= 728:
        return "Railroad Board"
    elif 729 <= area <= 733:
        return "Enumeration at Entry"
    else:
        return "Not issued."
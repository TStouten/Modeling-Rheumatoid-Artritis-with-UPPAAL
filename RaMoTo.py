import subprocess
import xml.etree.ElementTree as ET
import os
import sys

def ShowProtocol():
    lines = InternalProtocol.split('\n')
    total_weeks = (int(lines[0].split()[4]))
    initialStep = lines[2].split()[3]
    protocol_step = {}
    week_settings = {}
    med_settings = {}
    nextmed_settings = {}

    for x in range(6, len(lines)):
        if len(nextmed_settings) >= total_weeks * 4:
            break
        if "if (medp" in lines[x]:
            protocol_step.update({x: int(lines[x].split()[3])})
        if "weekdeadline" in lines[x]:
            week_settings.update({x: int(lines[x].split()[2])})
        if "medicineCombination" in lines[x]:
            med_settings.update({x: int(lines[x].split()[2])})
        if "medicationPackage" in lines[x]:
            nextmed_settings.update({x: int(lines[x].split()[2])})
    ConfirmSettings = []
    total_keys = len(week_settings.items())
    for cur_key, cur_val in med_settings.items():
        ConfirmSettings.append(
            "protocol step " + str(protocol_step.get(cur_key - 3)) + " has a duration of " + str(
                week_settings.get(cur_key + 1)) + " weeks, used medication is: " +
            str(med_settings.get(cur_key)) + " and next protocol step is: high: " +
            str(nextmed_settings.get(cur_key + 12)) + " moderate: " +
            str(nextmed_settings.get(cur_key + 9)) + " Low: " +
            str(nextmed_settings.get(cur_key + 6)) + " Remission: " + str(
                nextmed_settings.get(cur_key + 3)))
    print("\nInitial step is " + initialStep)
    print("\n".join(ConfirmSettings))
    print("\n")



while True:
    while True:
        patient = input("Patient model: ")
        if os.path.isfile(patient):
            break
    while True:
        protocol = input("Protocol model: ")
        if os.path.isfile(protocol):
            break
    while True:
        queries = input("Query file: ")
        if os.path.isfile(queries):
            break

    patientTree = ET.parse(patient)
    patientRoot = patientTree.getroot()
    protocolTree = ET.parse(protocol)
    protocolRoot = protocolTree.getroot()
    InternalProtocol = protocolRoot.find('declaration').text
    # Split protocol in lines, to read the number of medicine combinations and store this as a variable.
    InternalPatient = patientRoot.find('template').find('declaration').text
    InternalDeclaration = patientRoot.find('declaration').text


    running = True
    if running:
        continuing = True
        while continuing:
            choice = input("0 to run queries\n1 to show current protocol\n2 to edit existing protocol with new step "
                           "setting\n3 to delete a protocol step\n4 to add a protocol step\n5 Show all medicine combinations"
                           " \n6 Edit a medicine combinations\n7 Add a medicine combinations\n8 Show all queries\n")
            # Change nr of weeks and go to verifyta
            if choice == "0":
                lines = InternalDeclaration.split('\n')
                templine = lines[2].split()
                if (input("The queries will be run for " + templine[4] + " weeks, want to edit this?") == "y"):
                    while True:
                        newNum = input("Insert number of weeks")
                        if newNum.isdigit():
                            templine[4] = newNum
                            lines[2] = " ".join(templine)
                            InternalDeclaration = "\n".join(lines)
                            patientRoot.find('declaration').text = InternalDeclaration
                            break
                if (input("want to save patient and protocol files?") == "y"):
                    patientTree.write('PatientOutput.xml')
                    with open("PatientOutput.xml", "r") as f:
                        lines = f.readlines()
                        lines.insert(0, '<?xml version="1.0" encoding="utf-8"?>\n')
                        lines.insert(1,
                                     "<!DOCTYPE nta PUBLIC '-//Uppaal Team//DTD Flat System 1.1//EN' 'http://www.it.uu.se/research/group/darts/uppaal/flat-1_2.dtd'>\n")

                    with open("PatientOutput.xml", "w") as f:
                        text = "".join(lines)
                        f.write(text)
                    protocolTree.write('ProtocolOutput.xml')
                    with open("ProtocolOutput.xml", "r") as f:
                        lines = f.readlines()
                        lines.insert(0, '<?xml version="1.0" encoding="utf-8"?>\n')
                        lines.insert(1,
                                     "<!DOCTYPE nta PUBLIC '-//Uppaal Team//DTD Flat System 1.1//EN' 'http://www.it.uu.se/research/group/darts/uppaal/flat-1_2.dtd'>\n")

                    with open("ProtocolOutput.xml", "w") as f:
                        text = "".join(lines)
                        f.write(text)
                patientRoot.insert(1, protocolRoot)
                patientTree.write('output.xml')
                subprocess.run(["verifyta.exe", 'output.xml', queries])
                if (input("want to exit?") == "y"):
                    sys.exit()

            # Show protocol steps
            elif choice == "1":
                ShowProtocol()
            # edit steps
            elif choice == "2":
                while (input("change a protocol step?: ") == "y"):
                    lines = InternalProtocol.split('\n')
                    total_weeks = (int(lines[0].split()[4]))
                    initialStep = lines[2].split()[3]
                    protocol_step = {}
                    week_settings = {}
                    med_settings = {}
                    nextmed_settings = {}

                    for x in range(6, len(lines)):
                        if len(nextmed_settings) >= total_weeks * 4:
                            break
                        if "if (medp" in lines[x]:
                            protocol_step.update({x: int(lines[x].split()[3])})
                        if "weekdeadline" in lines[x]:
                            week_settings.update({x: int(lines[x].split()[2])})
                        if "medicineCombination" in lines[x]:
                            med_settings.update({x: int(lines[x].split()[2])})
                        if "medicationPackage" in lines[x]:
                            nextmed_settings.update({x: int(lines[x].split()[2])})
                    ConfirmSettings = []
                    total_keys = len(week_settings.items())
                    for cur_key, cur_val in med_settings.items():
                        ConfirmSettings.append(
                            "protocol step " + str(protocol_step.get(cur_key - 3)) + " has a duration of " + str(
                                week_settings.get(cur_key + 1)) + " weeks, used medication is: " +
                            str(med_settings.get(cur_key)) + " and next protocol step is: high: " +
                            str(nextmed_settings.get(cur_key + 12)) + " moderate: " +
                            str(nextmed_settings.get(cur_key + 9)) + " Low: " +
                            str(nextmed_settings.get(cur_key + 6)) + " Remission: " + str(
                                nextmed_settings.get(cur_key + 3)))
                    print("initial protocol step: " + initialStep)
                    print("\n".join(ConfirmSettings))
                    print("\n")
                    tochange = -1
                    while (tochange == -1):
                        tempChoice = input(
                            "which step do you want to edit, 0 is to change the initial protocol step?: ")
                        if tempChoice.isdigit():
                            tochange = int(tempChoice)
                    if tochange == 0:
                        tempInitial = input("insert new initial protocol step")
                        if tempInitial.isdigit():
                            tempLineList = lines[2].split()
                            tempLineList[3] = str(tempInitial)
                            current = " ".join(tempLineList)
                            lines[2] = current
                        else:
                            print("No valid initial step has been given\n")
                    elif tochange in list(protocol_step.values()):
                        key = list(protocol_step.keys())[list(protocol_step.values()).index(tochange)]
                        newWeek = input("insert duration for protocol step " + str(
                            protocol_step.get(key)) + " which is currently " + str(
                            week_settings.get(key + 4)) + " weeks:")
                        if not newWeek.isdigit():
                            newWeek = str(week_settings.get(key + 4))
                        newMed = input("insert medication for protocol step " + str(
                            protocol_step.get(key)) + " which is currently " + str(med_settings.get(key + 3)) + ":")
                        if not newMed.isdigit():
                            newMed = str(med_settings.get(key + 3))
                        newNextHigh = input("insert next protocol step for protocol step " + str(
                            protocol_step.get(key)) + " when in High which is currently " + str(
                            nextmed_settings.get(key + 15)) + ":")
                        if not newNextHigh.isdigit():
                            newNextHigh = str(nextmed_settings.get(key + 15))
                        newNextMod = input("insert next protocol step for protocol step " + str(
                            protocol_step.get(key)) + " when in moderate which is currently " + str(
                            nextmed_settings.get(key + 12)) + ":")
                        if not newNextMod.isdigit():
                            newNextMod = str(nextmed_settings.get(key + 12))
                        newNextLow = input("insert next protocol step for protocol step " + str(
                            protocol_step.get(key)) + " when in low which is currently " + str(
                            nextmed_settings.get(key + 9)) + ":")
                        if not newNextLow.isdigit():
                            newNextLow = str(nextmed_settings.get(key + 9))
                        newNextRem = input("insert next protocol step for protocol step " + str(
                            protocol_step.get(key)) + " when in remission which is currently " + str(
                            nextmed_settings.get(key + 6)) + ":")
                        if not newNextRem:
                            newNextRem = str(nextmed_settings.get(key + 6))
                        if newWeek.isdigit() and newMed.isdigit() and newNextHigh.isdigit() and newNextMod.isdigit() and newNextLow.isdigit() and newNextRem.isdigit():
                            med_settings.update({key + 3: newMed})
                            week_settings.update({key + 4: newWeek})
                            nextmed_settings.update({key + 15: newNextHigh})
                            nextmed_settings.update({key + 12: newNextMod})
                            nextmed_settings.update({key + 9: newNextLow})
                            nextmed_settings.update({key + 6: newNextRem})
                    ConfirmSettings = []
                    for cur_key, cur_val in med_settings.items():
                        ConfirmSettings.append(
                            "protocol step " + str(protocol_step.get(cur_key - 3)) + " has a duration of " + str(
                                week_settings.get(cur_key + 1)) + " weeks, used medication is: " +
                            str(med_settings.get(cur_key)) + " and next protocol step is: high: " +
                            str(nextmed_settings.get(cur_key + 12)) + " moderate: " +
                            str(nextmed_settings.get(cur_key + 9)) + " Low: " +
                            str(nextmed_settings.get(cur_key + 6)) + " Remission: " + str(
                                nextmed_settings.get(cur_key + 3)))
                    print("initial protocol step: " + lines[2].split()[3])
                    print("\n".join(ConfirmSettings))
                    print("\n")
                    print("")

                    if (input("is this correct?: ") == "y"):
                        for cur_key, cur_val in med_settings.items():
                            tempLineList = lines[cur_key].split()
                            tempLineList[2] = str(med_settings.get(cur_key))
                            current = " ".join(tempLineList)
                            lines[cur_key] = current
                            tempLineList = lines[cur_key + 1].split()
                            tempLineList[2] = str(week_settings.get(cur_key + 1))
                            current = " ".join(tempLineList)
                            lines[cur_key + 1] = current
                            tempLineList = lines[cur_key + 3].split()
                            tempLineList[2] = str(nextmed_settings.get(cur_key + 3))
                            current = " ".join(tempLineList)
                            lines[cur_key + 3] = current
                            tempLineList = lines[cur_key + 6].split()
                            tempLineList[2] = str(nextmed_settings.get(cur_key + 6))
                            current = " ".join(tempLineList)
                            lines[cur_key + 6] = current
                            tempLineList = lines[cur_key + 9].split()
                            tempLineList[2] = str(nextmed_settings.get(cur_key + 9))
                            current = " ".join(tempLineList)
                            lines[cur_key + 9] = current
                            tempLineList = lines[cur_key + 12].split()
                            tempLineList[2] = str(nextmed_settings.get(cur_key + 12))
                            current = " ".join(tempLineList)
                            lines[cur_key + 12] = current
                        InternalProtocol = "\n".join(lines)
                        protocolRoot.find('declaration').text = InternalProtocol
                        break
            # delete step
            elif choice == "3":
                while input("Delete a protocol step?: ") == "y":
                    lines = InternalProtocol.split('\n')
                    total_weeks = (int(lines[0].split()[4]))
                    protocol_step = {}
                    week_settings = {}
                    med_settings = {}
                    nextmed_settings = {}

                    for x in range(6, len(lines)):
                        if len(nextmed_settings) >= total_weeks * 4:
                            break
                        if "if (medp" in lines[x]:
                            protocol_step.update({x: int(lines[x].split()[3])})
                        if "weekdeadline" in lines[x]:
                            week_settings.update({x: int(lines[x].split()[2])})
                        if "medicineCombination" in lines[x]:
                            med_settings.update({x: int(lines[x].split()[2])})
                        if "medicationPackage" in lines[x]:
                            nextmed_settings.update({x: int(lines[x].split()[2])})
                    ConfirmSettings = []
                    total_keys = len(week_settings.items())
                    for cur_key, cur_val in med_settings.items():
                        ConfirmSettings.append(
                            "protocol step " + str(protocol_step.get(cur_key - 3)) + " has a duration of " + str(
                                week_settings.get(cur_key + 1)) + " weeks, used medication is: " +
                            str(med_settings.get(cur_key)) + " and next protocol step is: high: " +
                            str(nextmed_settings.get(cur_key + 12)) + " moderate: " +
                            str(nextmed_settings.get(cur_key + 9)) + " Low: " +
                            str(nextmed_settings.get(cur_key + 6)) + " Remission: " + str(
                                nextmed_settings.get(cur_key + 3)))

                    print("\n".join(ConfirmSettings))
                    print("\n")
                    toDelete = -1
                    while (toDelete == -1):
                        tempDelete = input("which step do you want to delete?: ")
                        if tempDelete.isdigit():
                            toDelete = int(tempDelete)
                    if (input("remove step: " + str(toDelete) + "?") == "y"):
                        for cur_key, cur_val in med_settings.items():
                            if protocol_step.get(cur_key - 3) == toDelete:
                                for deleting in range(0, 19):
                                    lines.pop(cur_key - 3)
                                lines[0] = "const int medcombinations = " + str(total_weeks - 1) + " ;"
                        InternalProtocol = "\n".join(lines)
                        protocolRoot.find('declaration').text = InternalProtocol
            # add a protocol step
            elif choice == "4":
                lines = InternalProtocol.split('\n')
                total_weeks = (int(lines[0].split()[4]))
                protocol_step = {}
                week_settings = {}
                med_settings = {}
                nextmed_settings = {}

                for x in range(6, len(lines)):
                    if len(nextmed_settings) >= total_weeks * 4:
                        break
                    if "if (medp" in lines[x]:
                        protocol_step.update({x: int(lines[x].split()[3])})
                    if "weekdeadline" in lines[x]:
                        week_settings.update({x: int(lines[x].split()[2])})
                    if "medicineCombination" in lines[x]:
                        med_settings.update({x: int(lines[x].split()[2])})
                    if "medicationPackage" in lines[x]:
                        nextmed_settings.update({x: int(lines[x].split()[2])})
                ConfirmSettings = []
                total_keys = len(week_settings.items())
                for cur_key, cur_val in med_settings.items():
                    ConfirmSettings.append(
                        "protocol step " + str(protocol_step.get(cur_key - 3)) + " has a duration of " + str(
                            week_settings.get(cur_key + 1)) + " weeks, used medication is: " +
                        str(med_settings.get(cur_key)) + " and next protocol step is: high: " +
                        str(nextmed_settings.get(cur_key + 12)) + " moderate: " +
                        str(nextmed_settings.get(cur_key + 9)) + " Low: " +
                        str(nextmed_settings.get(cur_key + 6)) + " Remission: " + str(
                            nextmed_settings.get(cur_key + 3)))

                print("\n".join(ConfirmSettings))
                print("\n")
                inputting = False
                if input("Add a step?") == "y":
                    inputting = True
                while inputting:
                    while True:
                        newStep = input("insert new step number")
                        if newStep.isdigit() and int(newStep) not in protocol_step.values():break
                    while True:
                        newWeek = input("insert duration")
                        if newWeek.isdigit():break
                    while True:
                        newMed = input("insert medication")
                        if newMed.isdigit():break
                    while True:
                        newNextHigh = input("insert next protocol step high")
                        if newNextHigh.isdigit():break
                    while True:
                        newNextMod = input("insert next protocol step moderate")
                        if newNextMod.isdigit():break
                    while True:
                        newNextLow = input("insert next protocol step low")
                        if newNextLow.isdigit():break
                    while True:
                        newNextRem = input("insert next protocol step remission")
                        if newNextRem.isdigit():break
                    selection = input(
                        "new protocol step " + newStep + " has a duration of " + newWeek + " with medication " + newMed + " next step high is " + newNextHigh + " next step moderate is " + newNextMod + " next step low is " + newNextLow + " next step remission is " + newNextRem + "\n is this correct?")
                    if selection == "y":
                        newProtocolStep = ["}", "medicineChange = 1 ;", "}",
                                           "medicationPackage = " + str(newNextHigh) + " ;", "else if (State==4){", "}",
                                           "medicationPackage = " + str(newNextMod) + " ;", "else if (State==3){", "}",
                                           "medicationPackage = " + str(newNextLow) + " ;", "else if (State==2){", "}",
                                           "medicationPackage = " + str(newNextRem) + " ;", "if (State==1){",
                                           "weekdeadline = " + str(newWeek) + " ;",
                                           "medicineCombination = " + str(newMed) + " ;", "weekstable = 0 ;",
                                           "weekmed = " + str(newWeek) + " ;", "if (medp == " + str(newStep) + " ){"]
                        for l in newProtocolStep:
                            lines.insert(6, l)
                        lines[0] = "const int medcombinations = " + str(total_weeks + 1) + " ;"
                        InternalProtocol = "\n".join(lines)
                        protocolRoot.find('declaration').text = InternalProtocol
                        break
                    else:
                        if input("try again?") != "y":
                            inputting = False
            # read medpacks
            elif choice == "5":
                lines = InternalPatient.split('\n')
                total_combinations = (int(lines[0].split()[4]))
                medications = {}
                medicine = {}
                for x in range(0, len(lines)):
                    if len(medicine) == total_combinations:
                        break
                    if "if (medpack == " in lines[x]:

                        templine = lines[x].split()
                        res = []
                        medicine.update({int(templine[3]): lines[
                            x + total_combinations - int(templine[3]) + 5 + int(templine[3]) * 14].split()[1]})
                        res.append(x)
                        res.append(templine[3])
                        res.append(templine[6])
                        for variable in range(0, 11):
                            # curent position+nr of medicince-mednr to return to closing bracket setCost + 6 to get to "next = 0" +
                            res.append(lines[x + total_combinations - int(templine[3]) + 6 + int(
                                templine[3]) * 14 + variable].split()[2])
                        medications.update({lines[x + total_combinations - int(templine[3]) + 5 + int(
                            templine[3]) * 14].split()[1]: res})
                for key, value in medicine.items():
                    print(str(key) + " : " + value)
                print("\n")
                choice = input(
                    "Input number to see specific settings or write all to see a detailed list for that medication combination")
                if choice.isdigit() and int(choice) >= 0 and int(choice) < total_combinations:
                    choicemed = medicine.get(int(choice))
                    medlist = medications.get(choicemed)
                    print(choicemed + "\nhas a cost of " + medlist[2] + " euro per week\nhigh to high: " + medlist[
                        3] + "\nhigh to moderate: " + medlist[4] + "\nmoderate to high: " + medlist[
                              5] + "\nmoderate to moderate: " + medlist[6] + "\nmoderate to low: " + medlist[
                              7] + "\nlow to moderate: " + medlist[8] + "\nlow to low: " + medlist[
                              9] + "\nlow to remission: " + medlist[10] + "\nremission to low: " + medlist[
                              11] + "\nremission to remission: " + medlist[12] + "\nstop weight: " + medlist[
                              13] + "\n\n")
                if choice == "all":
                    for x in range(0, total_combinations):
                        choicemed = medicine.get(int(x))
                        medlist = medications.get(choicemed)
                        print(choicemed + "\nhas a cost of " + medlist[2] + " euro per week\nhigh to high: " + medlist[
                            3] + "\nhigh to moderate: " + medlist[4] + "\nmoderate to high: " + medlist[
                                  5] + "\nmoderate to moderate: " + medlist[6] + "\nmoderate to low: " + medlist[
                                  7] + "\nlow to moderate: " + medlist[8] + "\nlow to low: " + medlist[
                                  9] + "\nlow to remission: " + medlist[10] + "\nremission to low: " + medlist[
                                  11] + "\nremission to remission: " + medlist[12] + "\nstop weight: " + medlist[
                                  13] + "\n\n")
            # Edit medpacks
            elif choice == "6":
                lines = InternalPatient.split('\n')
                total_combinations = (int(lines[0].split()[4]))
                print(total_combinations)
                medications = {}
                medicine = {}
                for x in range(0, len(lines)):
                    if len(medicine) == total_combinations:
                        break
                    if "if (medpack == " in lines[x]:

                        templine = lines[x].split()
                        res = []
                        medicine.update({int(templine[3]): lines[
                            x + total_combinations - int(templine[3]) + 5 + int(templine[3]) * 14].split()[1]})
                        res.append(x)
                        res.append(templine[3])
                        res.append(templine[6])
                        for variable in range(0, 11):
                            # curent position+nr of medicince-mednr to return to closing bracket setCost + 6 to get to "next = 0" +
                            res.append(lines[x + total_combinations - int(templine[3]) + 6 + int(
                                templine[3]) * 14 + variable].split()[2])
                        medications.update(
                            {lines[x + total_combinations - int(templine[3]) + 5 + int(templine[3]) * 14].split()[
                                 1]: res})

                for key, value in medicine.items():
                    print(value)
                while True:
                    # Change the medication
                    choosenMedication = input("Medication to change: ")
                    if (choosenMedication in medicine.values()):
                        medPosition = list(medicine.keys())[list(medicine.values()).index(choosenMedication)]
                        valueList = medications.get(choosenMedication)
                        newname = choosenMedication
                        print("\n" + choosenMedication + "\nhas a cost of " + valueList[
                            2] + " euro per week\nhigh to high: " + valueList[
                                  3] + "\nhigh to moderate: " + valueList[4] + "\nmoderate to high: " + valueList[
                                  5] + "\nmoderate to moderate: " + valueList[6] + "\nmoderate to low: " + valueList[
                                  7] + "\nlow to moderate: " + valueList[8] + "\nlow to low: " + valueList[
                                  9] + "\nlow to remission: " + valueList[10] + "\nremission to low: " + valueList[
                                  11] + "\nremission to remission: " + valueList[12] + "\nstop weight: " + valueList[
                                  13] + "\n\n")
                        if input("Want to change the medication name that is currently " + newname + " ?") == "y":
                            while True:
                                tempName = input("Insert new name")
                                if tempName == newname or not tempName in medicine.values():
                                    if tempName != "":
                                        newname = tempName
                                    break

                        printOptions = ["", "", "Cost of current medication: ",
                                        "Stay in high with the current weight of: ",
                                        "High to moderate with the current weight of: ",
                                        "Moderate to high with the current weight of: ",
                                        "Stay in moderate with the current weight of: ",
                                        "Moderate to low with the current weight of: ",
                                        "Low to moderate with the current weight of: ",
                                        "Stay in low with the current weight of: ",
                                        "Low to remission with the current weight of: ",
                                        "Remission to low with the current weight of: ",
                                        "Stay in remission with the current weight of: ",
                                        "Stop with the current weight of: "]
                        newSetting = []
                        newSetting.append(valueList[0])
                        newSetting.append(valueList[1])
                        for variable in range(2, 14):
                            gate = True
                            while gate:
                                newNum = input(printOptions[variable] + valueList[variable])
                                if newNum.isdigit():
                                    newSetting.append(newNum)
                                    break
                                elif newNum == "":
                                    newSetting.append(valueList[variable])
                                    break
                        print("\n" + newname + "\nhas a cost of " + newSetting[
                            2] + " euro per week\nhigh to high: " + newSetting[
                                  3] + "\nhigh to moderate: " + newSetting[4] + "\nmoderate to high: " + newSetting[
                                  5] + "\nmoderate to moderate: " + newSetting[6] + "\nmoderate to low: " + newSetting[
                                  7] + "\nlow to moderate: " + newSetting[8] + "\nlow to low: " + newSetting[
                                  9] + "\nlow to remission: " + newSetting[10] + "\nremission to low: " + newSetting[
                                  11] + "\nremission to remission: " + newSetting[12] + "\nstop weight: " + newSetting[
                                  13] + "\n\n")
                        if input("Is this correct? ") == "y":

                            baseline = newSetting[0]

                            tempLineList = lines[baseline].split()
                            tempLineList[6] = newSetting[2]
                            current = " ".join(tempLineList)
                            lines[baseline] = current

                            medNameLine = baseline + total_combinations - int(newSetting[1]) + 6 + int(
                                newSetting[1]) * 14 - 1
                            tempLineList = lines[medNameLine].split()
                            tempLineList[1] = newname
                            current = " ".join(tempLineList)
                            lines[medNameLine] = current
                            for variable in range(0, 11):
                                toEdit = baseline + total_combinations - int(newSetting[1]) + 6 + int(
                                    newSetting[1]) * 14 + variable
                                tempLineList = lines[toEdit].split()
                                tempLineList[2] = newSetting[variable + 3]
                                current = " ".join(tempLineList)
                                lines[toEdit] = current
                            print("Will be updated")
                            InternalPatient = "\n".join(lines)
                            # for l in lines:
                            #     print(l)
                            patientRoot.find('template').find('declaration').text = InternalPatient

                            break
                        elif input("want to try again? ") != "y":
                            break
            # Add a new medpack
            elif choice == "7":
                lines = InternalPatient.split('\n')
                total_combinations = (int(lines[0].split()[4]))
                medicine = {}
                for x in range(0, len(lines)):
                    if len(medicine) == total_combinations:
                        break
                    if "if (medpack == " in lines[x]:
                        templine = lines[x].split()
                        medicine.update({int(templine[3]): lines[
                            x + total_combinations - int(templine[3]) + 5 + int(templine[3]) * 14].split()[1]})
                for key, value in medicine.items():
                    print(value)
                newName = ""
                while True:
                    tempName = input("Please insert the name for the new Medication")
                    if tempName != "" and tempName not in medicine.values():
                        newName = tempName
                        break

                printOptions = ["", "", "Cost of current medication: ", "Stay in high with the current weight of: ",
                                "High to moderate with the current weight of: ",
                                "Moderate to high with the current weight of: ",
                                "Stay in moderate with the current weight of: ",
                                "Moderate to low with the current weight of: ",
                                "Low to moderate with the current weight of: ",
                                "Stay in low with the current weight of: ",
                                "Low to remission with the current weight of: ",
                                "Remission to low with the current weight of: ",
                                "Stay in remission with the current weight of: ", "Stop with the current weight of: "]
                newSetting = []
                # position in file
                newSetting.append(5 + total_combinations)
                # medication number
                newSetting.append(str(total_combinations))
                for variable in range(2, 14):
                    gate = True
                    while gate:
                        newNum = input(printOptions[variable])
                        if newNum.isdigit():
                            newSetting.append(newNum)
                            break
                print(newSetting)
                lines[0] = "const int MedicineCombinations = " + str(int(lines[0].split()[4]) + 1) + " ;"
                lines.insert(5 + total_combinations,
                             "if (medpack == " + str(newSetting[1]) + " ){weeklyCost = " + newSetting[2] + " ;}")
                newlines = []
                newlines.append("if (medpack == " + newSetting[1] + "){")
                newlines.append("// " + newName)
                newlines.append("if (next==0){returnValue= " + newSetting[3] + " ;}")
                newlines.append("if (next==1){returnValue= " + newSetting[4] + " ;}")
                newlines.append("if (next==2){returnValue= " + newSetting[5] + " ;}")
                newlines.append("if (next==3){returnValue= " + newSetting[6] + " ;}")
                newlines.append("if (next==4){returnValue= " + newSetting[7] + " ;}")
                newlines.append("if (next==5){returnValue= " + newSetting[8] + " ;}")
                newlines.append("if (next==6){returnValue= " + newSetting[9] + " ;}")
                newlines.append("if (next==7){returnValue= " + newSetting[10] + " ;}")
                newlines.append("if (next==8){returnValue= " + newSetting[11] + " ;}")
                newlines.append("if (next==9){returnValue= " + newSetting[12] + " ;}")
                newlines.append("if (next==10){if(medchange==1){returnValue= " + newSetting[13] + " ;}}")
                newlines.append("}")
                lineIncreaser = 0
                for x in range(0, len(newlines)):
                    lines.insert(5 + total_combinations + 5 + 14 * total_combinations + x, newlines[x])

                InternalPatient = "\n".join(lines)
                patientRoot.find('template').find('declaration').text = InternalPatient
            # read queries
            elif choice == "8":
                with open(queries) as f:
                    lines = f.readlines()
                    print(len(lines))
                    for x in range(0, len(lines)):
                        print(str(x) + ": " + lines[x])
                    if (input("Want to edit a query?") == "y"):
                        choice = input("insert the number of the query: ")
                        if choice.isdigit() and int(choice) in range(0, len(lines)):
                            tempquery = lines[int(choice)].split()
                            totalRuns = input("how many simulations for this query?")
                            if totalRuns.isdigit():
                                tempquery[1] = totalRuns
                                current = " ".join(tempquery)
                                lines[int(choice)] = current + "\n"

                    for x in range(0, len(lines)):
                        print(str(x) + lines[x])
                    file = open(queries, "w")
                    for l in lines:
                        file.write(l)
                    file.close()





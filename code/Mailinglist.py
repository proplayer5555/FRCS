from Sensor import *
import os

class mailing_system:
    def __init__(self):
        pass

    def create_mailing_list(self,criticallist):
        current_dir = os.getcwd()
        stringis = f"Dear recipients, please exercise extreme caution near the following forests:"
        namelist = []
        full_list1 = []
        full_list2 = []
        full_list3 = []
        for item in criticallist:
            namelist.append(item[0].getname())
            full_list1.append("{:.2f}".format(float(item[1])))
            full_list2.append("{:.2f}".format(float(item[2])))
            full_list3.append(item[0].printall())
        if not os.path.exists(current_dir + "/Mailinglist"):
            os.makedirs(current_dir + "/Mailinglist")
        output_file = os.path.join(current_dir, 'Mailinglist', 'Mailinglist.txt')
        with open(output_file, 'w', encoding="utf-8") as file:
            file.write(stringis)
            file.write('\n')  # Write a newline after the stringis
            for name in namelist:
                file.write(name)
                file.write('\n')
            file.write("\nPlease take the following precautions immediately:\n\n1.Stay informed: Listen to local news updates, radio broadcasts, or check official social media channels "
                       "for the latest updates on the fire's progression, evacuation orders, and safety guidelines.\n\n2.Pack an emergency kit: Prepare a bag with essential "
                       "items such as non-perishable food, drinking water, medications, clothing, important documents, flashlights, and batteries. Keep this kit readily accessible in case of evacuation."
                       "\n\n3.Create a defensible space: Clear any dry vegetation or debris from your property to create a buffer zone between your home and the approaching fire. "
                       "Trim overhanging tree branches and remove flammable materials from your yard.\n\n4.Evacuation plan: Familiarize yourself with evacuation routes and know multiple "
                       "ways to exit your neighborhood. If instructed to evacuate, leave immediately, following the designated routes and guidelines provided by local authorities.\n\n5.Monitor "
                       "air quality: Forest fires can produce hazardous smoke and pollutants. Stay indoors as much as possible and use air purifiers or create a clean air room by sealing windows "
                       "and doors with damp towels to prevent smoke infiltration.\n\n6.Keep communication devices charged: Ensure your mobile phones, radios, and other communication devices "
                       "are fully charged and keep spare batteries or power banks handy. Regularly check for emergency alerts and stay in touch with friends, family, and neighbors.\n\n7."
                       "Be vigilant and report fires: If you notice any signs of fire or smoke, promptly report it to the emergency services. Do not attempt to extinguish a large "
                       "fire yourself; instead, focus on your safety and follow evacuation procedures.\n\n8.Follow official instructions: Pay close attention to instructions and warnings "
                       "issued by local authorities and emergency services. Cooperate fully with their directives and respect any mandatory evacuation orders for your safety.\n\nRemember, "
                       "in times of emergency, it is crucial to remain calm and act swiftly. Look out for your neighbors, especially those who may require assistance, and together, we can "
                       "overcome this challenge.\n\nWe will continue to monitor the situation closely and provide updates as necessary. For further information and updates, please visit our website "
                       "at cindersoft.org/wedontcare.\n\nStay safe and take all necessary precautions to protect yourself and your loved ones.\n")
        output_file = os.path.join(current_dir, 'Mailinglist', 'OfficialMailinglist.txt')
        
        with open(output_file, 'w', encoding="utf-8") as file:
            file.write(stringis)
            file.write('\n')  # Write a newline after the stringis
            for item1, item2, item3 in zip(full_list1, full_list2, full_list3):
                file.write("FDI: ")
                file.write(item1)
                file.write('\t\t')
                file.write("ROF: ")
                file.write(item2)
                file.write('\t\t')
                file.write(item3)
                file.write('\n\n')

        return f"\nNotification sent successfully"
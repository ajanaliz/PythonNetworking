__author__ = 'Ali J'
"""
    Simple Subnet Calculator to calculate the number of valid hosts per subnet,
    wildcard ip, network address and broadcast address in my GNS3 Server
"""
import sys, random


def subnet_calc():
    try:
        while True:
            ip_address = input("Enter ip address:")
            print(ip_address)

            # splitting into octet
            a = ip_address.split('.')
            # print(a)
            # print(type(a[0]))

            if (len(a) == 4) and (1 <= int(a[0]) <= 223) and (int(a[0]) != 127) and (
                            int(a[0]) != 169 or int(a[1]) != 254) and (
                                    0 <= int(a[1]) <= 255 and 0 <= int(a[2]) <= 255 and 0 <= int(a[3]) <= 255):
                #  print("valid ip address")
                break
            else:
                print("Invalid ip address. PLEASE TRY WITH VALID IP ADDRESS")
                continue
        masks = [255, 245, 252, 248, 240, 224, 192, 128, 0]

        # checking subnet validity
        while True:
            subnet_mask = input("enter the subnet mask:")
            # splitting into octet
            b = subnet_mask.split(".")
            # print(b)
            if (len(b) == 4) and (int(b[0]) == 255) and (int(b[1]) in masks) and (int(b[2]) in masks) and (
                        int(b[3]) in masks) and (int(b[0]) >= int(b[1]) >= int(b[2]) >= int(b[3])):
                break
            else:
                print("Invalid subnet mask . PLEASE TRY WITH VALID SUBNET")
                continue

        # converting subnet into binary
        # CONVERTING SUBNET INTO BINARY
        mask_octet = []  # empty list to store the  binary values
        mask_octet_decimal = subnet_mask.split(".")
        # print(mask_octet_decimal)

        for octet_index in range(0, len(mask_octet_decimal)):
            # print(bin(int(mask_octet_decimal[octet_index])))
            binary_octet = bin(int(mask_octet_decimal[octet_index])).split("b")[1]
            # print(binary_octet)

            if len(binary_octet) == 8:
                mask_octet.append(binary_octet)
            elif len(binary_octet) < 8:
                binary_octet_padded = binary_octet.zfill(8)
                mask_octet.append(binary_octet_padded)

        # print(mask_octet)
        decimal_subnet_joined = "".join(mask_octet)
        # print(decimal_subnet_joined)

        # calculating hostbit and number of host
        # host can be calculated by using 2^X -2 where X is the number of host bit
        #
        no_of_zero = decimal_subnet_joined.count("0")
        no_of_ones = 32 - no_of_zero
        no_of_host = abs(2 ** no_of_zero - 2)  # gives no of host

        # print(no_of_zero)
        # print(no_of_ones)
        # print(no_of_host)

        # obtaining wildcard octet subtract subnet from 255.255.255.255
        wildcard_octet = []
        for w_octet in mask_octet_decimal:
            # print(w_octet)
            wild_octet = 255 - int(w_octet)
            # print(wild_octet)
            wildcard_octet.append(str(wild_octet))
        # print(wildcard_octet)
        wildcard_mask = ".".join(wildcard_octet)
        # print(wildcard_mask)

        # CONVERTING IP INTO BINARY

        ip_octets_padded = []
        ip_octets_decimal = ip_address.split(".")

        for octet_index in range(0, len(ip_octets_decimal)):
            binary_octet = bin(int(ip_octets_decimal[octet_index])).split("b")[1]
            if len(binary_octet) < 8:
                binary_octet_padded = binary_octet.zfill(8)
                ip_octets_padded.append(binary_octet_padded)
            else:
                ip_octets_padded.append(binary_octet)
                # print(ip_octet_padded)
        binary_ip = "".join(ip_octets_padded)
        # print(binary_ip)

        # BOTAINING THE NETWORK AND BROADCAST ADDRESS FROM THE ABOVE OBTAINED BINARY
        network_address_binary = binary_ip[:(no_of_ones)] + "0" * no_of_zero
        # print(len(network_address_binary))

        broadcast_address_binary = binary_ip[:(no_of_ones)] + "1" * no_of_zero
        # print(broadcast_address_binary)

        net_ip_octets = []
        for octet in range(0, len(network_address_binary), 8):
            print(octet)
            net_ip_octet = network_address_binary[octet:octet + 8]
            net_ip_octets.append(net_ip_octet)

        # print(net_ip_octets)
        net_ip_address = []
        for each_octet in net_ip_octets:
            net_ip_address.append(str(int(each_octet)))
        # print(net_ip_address)

        network_address = ".".join(net_ip_address)
        # print(network_address)

        bst_ip_octets = []
        for octet in range(0, len(broadcast_address_binary), 8):
            bst_ip_octet = broadcast_address_binary[octet:octet + 8]
            bst_ip_octets.append(bst_ip_octet)
        # print(bst_ip_octets)

        bst_ip_address = []
        for each_octet in bst_ip_octets:
            bst_ip_address.append(str(int(each_octet, 2)))

        # print(bst_ip_address)
        broadcasr_address = ".".join(bst_ip_address)
        # print(broadcasr_address)

        # finalresult
        print
        "\n"
        print("Network address                     : %s " % network_address)
        print("Broadcast address                   : %s" % broadcasr_address)
        print("Number is valid Host per subnet     : %s" % no_of_host)
        print("Wildcard mask                       : %s" % wildcard_mask)
        print("Mask Bits                           : %s" % no_of_ones)
        print
        "\n"

        # Generation of random IP in subnet
        while True:
            generate = input("Generate random ip address from subnet? (y/n)")

            if generate == "y":
                generated_ip = []

                # Obtain available IP address in range, based on the difference between octets in broadcast address and network address
                for indexb, oct_bst in enumerate(bst_ip_address):
                    # print( indexb , oct_bst)
                    for indexn, oct_net in enumerate(net_ip_address):
                        # print(indexn , oct_net)
                        if indexb == indexn:
                            if oct_bst == oct_net:
                                #Add identical octets to the generated_ip list
                                generated_ip.append(oct_bst)
                            else:
                                #Generate random number(s) from within octet intervals and append them to the generated_ip list
                                generated_ip.append(str(random.randint(int(oct_net), int(oct_bst))))
                #IP address generated from the subnet pool
                # print(generated_ip)
                y_iaddr = ".".join(generated_ip)
                # print(y_iaddr)

                print("Random IP address is: %s" % y_iaddr)
                print("\n")
                continue
            else:
                print("Ok, bye!\n")
                break
    except Exception:
        print("\n\nProgram aborted by user. Exiting...\n")
        sys.exit()


subnet_calc()

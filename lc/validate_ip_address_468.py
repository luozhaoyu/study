class Solution:
    def isValidIPv4(self, queryIP):
        parts = queryIP.split(".")
        for part in parts:
            if not part.isdigit():
                return False
            
            if len(part) > 1 and part[0] == "0":  # check leading zero
                return False

            number = int(part)
            if number < 0 or number > 255:
                return False
        return True

    def isValidIPv6(self, queryIP):
        parts = queryIP.split(":")
        for part in parts:
            if len(part) <= 0 or len(part) > 4:
                return False

            for char in part:
                if not char.isalnum():
                    return False
                lower = char.lower()
                if lower > "f" and lower <= "z":
                    return False
        return True

    def validIPAddress(self, queryIP: str) -> str:
        if len(queryIP.split(".")) == 4:
            result = self.isValidIPv4(queryIP)
            if result:
                return "IPv4"
            else:
                return "Neither"

        if len(queryIP.split(":")) == 8:
            result = self.isValidIPv6(queryIP)
            if result:
                return "IPv6"
            else:
                return "Neither"
        return "Neither"
        
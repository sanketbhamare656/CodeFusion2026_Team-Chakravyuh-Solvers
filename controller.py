from urllib.parse import urlparse
import tldextract
import model
import time
import smtplib
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

class Controller:
    def __init__(self, user_email="sanketbhamare397@gmail.com"):
        self.BASE_SCORE = 75
        self.model = model
        self.user_email = user_email

    def is_banned_in_india(self, domain):
        banned_websites = [
            "thepiratebay.org", "kickass.to", "torrentz.eu", "1337x.to",
            "torrentz2.eu", "limetorrents.info", "yts.mx", "rarbg.to",
            "extratorrent.ag", "fmovies.to", "putlocker.is",
        ]
        return domain.lower() in banned_websites

    def send_alert(self, url, score, details):
        try:
            sender_email = os.getenv("EMAIL_SENDER", "your-email@gmail.com")
            sender_password = os.getenv("EMAIL_PASSWORD", "your-app-password")
            receiver_email = self.user_email
            detection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            subject = "Security Alert - Suspicious URL Detected"
            email_body = f"""
Dear PhishNet User,

A suspicious URL you scanned has been flagged due to a low trust score.

Scan Summary:
- URL: {url}
- Trust Score: {score}/100
- Scanned At: {detection_time}

Technical Details:
- Domain Age: {details.get("age", "N/A")}
- Domain Rank: {details.get("rank", "N/A")}
- IP Address: {details.get("ip", "N/A")}
- URL Shortened: {details.get("is_url_shortened", "N/A")}
- HSTS Support: {details.get("hsts_support", "N/A")}
- IP Present in URL: {details.get("ip_present", "N/A")}
- SSL Certificate: {details.get("ssl", "N/A")}
- URL Redirects: {details.get("url_redirects", "N/A")}
- URL Length: {details.get("too_long_url", "N/A")}
- URL Depth: {details.get("too_deep_url", "N/A")}
- WHOIS Data: {details.get("whois", "N/A")}

Recommendation:
Please avoid visiting this URL. It may be malicious or harmful.

Contact us at: phishnetmailservice@gmail.com
Best Regards,
PhishNet - A Digital Net Capturing Malicious Links
Developed by: Team Chakravyuh Solvers
https://sanketsportfolio.vercel.app/
"""

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            message.attach(MIMEText(email_body.encode("utf-8"), "plain", "utf-8"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, message.as_string())

            print(f"Security alert email sent to {receiver_email}")
        except Exception as e:
            print(f"Email sending failed: {e}")

    def main(self, url):
        try:
            url = self.model.include_protocol(url)
            domain_info = tldextract.extract(url)
            domain = f"{domain_info.domain}.{domain_info.suffix}"
            subdomain = domain_info.subdomain

            print(f"Checking URL: {url}")
            print(f"Extracted domain: {domain}")
            
            if self.is_banned_in_india(domain):
                time.sleep(5)
                print("The website is banned in India.")
                return {
                    "status": "BLOCKED",
                    "url": url,
                    "msg": f"The website '{domain}' is banned in India."
                }

            print("Validating URL format...")
            url_validation = self.model.validate_url(url)
            response = {"status": "SUCCESS", "url": url}
            trust_score = self.BASE_SCORE

            try:
                print("Checking PhishTank database...")
                if self.model.phishtank_search(url):
                    response["msg"] = "This is a verified phishing link."
                    trust_score -= 30
                    print("Phishing match found in PhishTank.")
            except Exception:
                print("PhishTank check failed.")

            response["response_status"] = url_validation

            try:
                print("Fetching domain rank...")
                domain_rank = self.model.get_domain_rank(domain)
                trust_score = self.model.calculate_trust_score(trust_score, "domain_rank", domain_rank)
                response["rank"] = domain_rank if domain_rank else "10,00,000+"
                print(f"Domain rank: {response['rank']}")
            except:
                print("Domain rank fetch failed.")

            try:
                print("Fetching WHOIS information...")
                whois_data = self.model.whois_data(domain)
                domain_age = whois_data["age"]
                trust_score = self.model.calculate_trust_score(trust_score, "domain_age", domain_age)
                response["age"] = domain_age if domain_age == "Not Given" else f"{round(domain_age, 1)} year(s)"
                response["whois"] = whois_data["data"]
                print(f"Domain age: {response['age']}")
                if domain_age != "Not Given":
                    trust_score += 10
                    print("WHOIS Bonus Applied: +10")
            except:
                print("WHOIS fetch failed.")

            try:
                print("Checking if URL is shortened...")
                is_url_shortened = self.model.is_url_shortened(url)
                trust_score = self.model.calculate_trust_score(trust_score, "is_url_shortened", is_url_shortened)
                response["is_url_shortened"] = is_url_shortened
                print(f"URL shortened: {is_url_shortened}")
            except:
                print("URL shortener check failed.")

            try:
                print("Checking HSTS support...")
                hsts_support = self.model.hsts_support(url)
                trust_score = self.model.calculate_trust_score(trust_score, "hsts_support", hsts_support)
                response["hsts_support"] = hsts_support
                print(f"HSTS support: {hsts_support}")
            except:
                print("HSTS check failed.")

            try:
                print("Checking if IP is present in URL...")
                ip_present = self.model.ip_present(url)
                trust_score = self.model.calculate_trust_score(trust_score, "ip_present", ip_present)
                response["ip_present"] = ip_present
                print(f"IP present in URL: {ip_present}")
            except:
                print("IP presence check failed.")

            try:
                print("Checking URL redirection...")
                url_redirects = self.model.url_redirects(url)
                trust_score = self.model.calculate_trust_score(trust_score, "url_redirects", url_redirects)
                response["url_redirects"] = url_redirects
                print(f"URL redirects: {url_redirects}")
            except:
                print("URL redirection check failed.")

            try:
                print("Checking URL length...")
                too_long_url = self.model.too_long_url(url)
                trust_score = self.model.calculate_trust_score(trust_score, "too_long_url", too_long_url)
                response["too_long_url"] = too_long_url
                print(f"Too long URL: {too_long_url}")
            except:
                print("URL length check failed.")

            try:
                print("Checking URL depth...")
                too_deep_url = self.model.too_deep_url(url)
                trust_score = self.model.calculate_trust_score(trust_score, "too_deep_url", too_deep_url)
                response["too_deep_url"] = too_deep_url
                print(f"Too deep URL: {too_deep_url}")
            except:
                print("URL depth check failed.")

            try:
                print("Fetching IP address...")
                ip = self.model.get_ip(domain)
                response["ip"] = "Unavailable" if ip == 0 else ip
                print(f"IP address: {response['ip']}")
            except:
                print("IP fetch failed.")

            try:
                print("Fetching SSL certificate...")
                ssl = self.model.get_certificate_details(domain)
                response["ssl"] = ssl
                print(f"SSL details: {ssl}")
                # SSL Bonus
                if ssl and ssl != 0:
                    trust_score += 15
                    print("SSL Bonus Applied: +15")
            except:
                print("SSL certificate check failed.")

            print("Checking for suspicious keywords...")
            suspicious_keywords = ["login", "secure", "verify", "account", "signin", "update"]
            if any(keyword in url.lower() for keyword in suspicious_keywords):
                trust_score -= 10
                print("Suspicious keywords found in URL.")

            if "trycloudflare.com" in domain:
                trust_score -= 20
                print("Tunnel domain detected (trycloudflare.com).")

            if len(subdomain.split("-")) > 2 or len(subdomain) > 30:
                trust_score -= 10
                print("Unusual subdomain structure detected.")
            # Clean URL Bonus
            if not response.get("ip_present"):
                trust_score += 5

            if not response.get("url_redirects"):
                trust_score += 5

            # HSTS Bonus
            if response.get("hsts_support") == 1:
                trust_score += 5

            # Suspicious Subdomain
            if self.model.suspicious_subdomain(subdomain):
                trust_score -= 15
                print("Suspicious Subdomain Detected: -15")
            trust_score = int(max(min(trust_score, 100), 0))
            response["trust_score"] = trust_score
            print(f"Final trust score: {trust_score}/100")

            if trust_score <= 80:
                print("Sending alert email...")
                self.send_alert(url, trust_score, response)

            return response

        except Exception as e:
            print(f"Error occurred during scanning: {e}")
            return {
                "status": "ERROR",
                "url": url,
                "msg": "Some error occurred, please check the URL.",
                "emsg": str(e),
            }

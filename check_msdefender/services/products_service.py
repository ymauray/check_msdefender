"""Products service implementation."""

from typing import Dict, Optional, Any
from datetime import datetime

from check_msdefender.core.exceptions import ValidationError
from check_msdefender.core.logging_config import get_verbose_logger


class ProductsService:
    """Service for checking installed products on machines."""

    def __init__(self, defender_client: Any, verbose_level: int = 0) -> None:
        """Initialize with Defender client."""
        self.defender = defender_client
        self.logger = get_verbose_logger(__name__, verbose_level)

    def get_result(
        self, machine_id: Optional[str] = None, dns_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get products result with value and details for a machine."""
        self.logger.method_entry("get_result", machine_id=machine_id, dns_name=dns_name)

        if not machine_id and not dns_name:
            raise ValidationError("Either machine_id or dns_name must be provided")

        # Get machine information
        target_dns_name = dns_name
        target_machine_id = machine_id

        if machine_id:
            # Get DNS name from machine_id
            machine_details = self.defender.get_machine_by_id(machine_id)
            target_dns_name = machine_details.get("computerDnsName", "Unknown")
        elif dns_name:
            # Get machine_id from dns_name
            dns_response = self.defender.get_machine_by_dns_name(dns_name)
            machines = dns_response.get("value", [])
            if not machines:
                raise ValidationError(f"Machine not found with DNS name: {dns_name}")
            target_machine_id = machines[0].get("id")
            target_dns_name = dns_name

        # Get products for the machine
        self.logger.info("Fetching products from Microsoft Defender")
        products_data = self.defender.get_products()
        all_products = products_data.get("value", [])
        products = [
            product for product in all_products if product.get("deviceId") == target_machine_id
        ]

        self.logger.info(f"Found {len(products)} CVE vulnerabilities for machine {target_dns_name}")

        # Group vulnerabilities by software
        software_vulnerabilities = {}
        for vulnerability in products:
            software_name = vulnerability.get("softwareName", "Unknown")
            software_version = vulnerability.get("softwareVersion", "Unknown")
            software_vendor = vulnerability.get("softwareVendor", "Unknown")
            cve_id = vulnerability.get("cveId", "Unknown")
            cvss_score = vulnerability.get("cvssScore", 0)
            disk_paths = vulnerability.get("diskPaths", [])
            severity = vulnerability.get("vulnerabilitySeverityLevel", "Unknown")

            software_key = f"{software_name}-{software_version}-{software_vendor}"

            if software_key not in software_vulnerabilities:
                software_vulnerabilities[software_key] = {
                    "name": software_name,
                    "version": software_version,
                    "vendor": software_vendor,
                    "cves": [],
                    "paths": set(),
                    "max_cvss": 0,
                    "severities": set(),
                }

            software_vulnerabilities[software_key]["cves"].append(cve_id)
            software_vulnerabilities[software_key]["paths"].update(disk_paths)
            software_vulnerabilities[software_key]["max_cvss"] = max(
                software_vulnerabilities[software_key]["max_cvss"], cvss_score
            )
            software_vulnerabilities[software_key]["severities"].add(severity)

        # Count vulnerabilities by severity
        critical_count = 0
        high_count = 0
        medium_count = 0
        low_count = 0

        for vulnerability in products:
            severity = vulnerability.get("vulnerabilitySeverityLevel", "Unknown").lower()
            if severity == "critical":
                critical_count += 1
            elif severity == "high":
                high_count += 1
            elif severity == "medium":
                medium_count += 1
            elif severity == "low":
                low_count += 1

        # Count vulnerable software for reporting
        vulnerable_software = []
        for software in software_vulnerabilities.values():
            if len(software["cves"]) > 0:
                vulnerable_software.append(software)

        # Create details for output
        details = []
        total_score = 0
        if software_vulnerabilities:
            summary_line = f"{len(products)} total CVEs (Critical: {critical_count}, High: {high_count}, Medium: {medium_count}, Low: {low_count}), {len(vulnerable_software)} vulnerable software"
            details.append(summary_line)

            score = 0
            # Add software details (limit to 10)
            for software in list(software_vulnerabilities.values())[:10]:
                cve_count = len(software["cves"])
                unique_cves = list(set(software["cves"]))
                cve_list = ", ".join(unique_cves[:5])  # Show first 5 CVEs
                severities = ", ".join(software["severities"])  # Show first 5 CVEs
                for severity_name in software["severities"]:
                    severity = severity_name.lower()
                    if severity == "critical":
                        score += 100
                    elif severity == "high":
                        score += 10
                    elif severity == "medium":
                        score += 5
                    elif severity == "low":
                        score += 1

                if len(unique_cves) > 5:
                    cve_list += f".. (+{len(unique_cves) - 5} more)"

                details.append(
                    f"{software['name']} {software['version']} ({software['vendor']}) - "
                    f"{score} ({cve_count}: {severities}) weaknesses ({cve_list})"
                )
                total_score += score
                # Add paths (limit to 4)
                for path in list(software["paths"])[:4]:
                    details.append(f" - {path}")

        # Determine the value based on severity:
        # - Critical vulnerabilities trigger critical threshold
        # - High/Medium vulnerabilities trigger warning threshold
        # - Low vulnerabilities or no vulnerabilities are OK
        result = {
            "value": total_score,
            "details": details,
            "vulnerable_count": len(vulnerable_software),
            "critical_count": critical_count,
            "high_count": high_count,
            "medium_count": medium_count,
            "low_count": low_count,
            "total_cves": len(products),
            "total_software": len(software_vulnerabilities),
        }

        self.logger.info(
            f"Products analysis complete: {len(products)} total CVEs "
            f"(Critical: {critical_count}, High: {high_count}, Medium: {medium_count}, Low: {low_count}), "
            f"{len(vulnerable_software)} vulnerable software"
        )
        self.logger.method_exit("get_result", result)
        return result

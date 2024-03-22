from prowler.lib.check.models import Check, Check_Report_Azure
from prowler.providers.azure.services.network.network_client import network_client


class network_bastion_host_exists(Check):
    def execute(self) -> Check_Report_Azure:
        findings = []
        for subscription, bastion_hosts in network_client.bastion_hosts.items():
            if not bastion_hosts:
                status = "FAIL"
                status_extended = (
                    f"Bastion Host from subscription {subscription} does not exist"
                )
                location = "N/A"
                resource_id = "N/A"
            else:
                bastion_names = ", ".join(
                    [bastion_host.name for bastion_host in bastion_hosts]
                )
                resource_id = ", ".join(
                    [bastion_host.id for bastion_host in bastion_hosts]
                )
                location = ", ".join(
                    [bastion_host.location for bastion_host in bastion_hosts]
                )
                status = "PASS"
                status_extended = f"Bastion Host from subscription {subscription} available are: {bastion_names}"

            report = Check_Report_Azure(self.metadata())
            report.subscription = subscription
            report.resource_name = "Bastion Host"
            report.resource_id = resource_id
            report.status = status
            report.location = location
            report.status_extended = status_extended
            findings.append(report)

        return findings

import {useState, useMemo} from "react";
import {format} from "date-fns";
import type {Campaign} from "@/types";
import {
    Table,
    TableHeader,
    TableBody,
    TableHead,
    TableRow,
    TableCell,
} from "@/components/ui/table";

interface CampaignTableProps {
    campaigns: Campaign[];
}

export function CampaignTable({campaigns}: CampaignTableProps) {
    const [filters, setFilters] = useState({
        campaign: "",
        platform: "",
        region: "",
    });

    const uniqueCampaigns = useMemo(() => {
        return [...new Set(campaigns.map((c) => c.campaign_name))];
    }, [campaigns]);

    const uniquePlatforms = useMemo(() => {
        return [...new Set(campaigns.map((c) => c.platform))];
    }, [campaigns]);

    const uniqueRegions = useMemo(() => {
        return [...new Set(campaigns.map((c) => c.region))];
    }, [campaigns]);

    const filteredCampaigns = useMemo(() => {
        return campaigns.filter((campaign) => {
            return (
                (filters.campaign === "" ||
                    campaign.campaign_name === filters.campaign) &&
                (filters.platform === "" || campaign.platform === filters.platform) &&
                (filters.region === "" || campaign.region === filters.region)
            );
        });
    }, [campaigns, filters]);

    return (
        <div className="space-y-4">
            <div className="flex flex-col space-y-4 md:flex-row md:space-x-4 md:space-y-0">
                <div className="w-full md:w-1/3">
                    <label className="text-sm font-medium">Campaign</label>
                    <select
                        className="w-full rounded-md border p-2"
                        value={filters.campaign}
                        onChange={(e) => setFilters({...filters, campaign: e.target.value})}
                    >
                        <option value="">All Campaigns</option>
                        {uniqueCampaigns.map((campaign) => (
                            <option key={campaign} value={campaign}>
                                {campaign}
                            </option>
                        ))}
                    </select>
                </div>
                <div className="w-full md:w-1/3">
                    <label className="text-sm font-medium">Platform</label>
                    <select
                        className="w-full rounded-md border p-2"
                        value={filters.platform}
                        onChange={(e) => setFilters({...filters, platform: e.target.value})}
                    >
                        <option value="">All Platforms</option>
                        {uniquePlatforms.map((platform) => (
                            <option key={platform} value={platform}>
                                {platform}
                            </option>
                        ))}
                    </select>
                </div>
                <div className="w-full md:w-1/3">
                    <label className="text-sm font-medium">Region</label>
                    <select
                        className="w-full rounded-md border p-2"
                        value={filters.region}
                        onChange={(e) => setFilters({...filters, region: e.target.value})}
                    >
                        <option value="">All Regions</option>
                        {uniqueRegions.map((region) => (
                            <option key={region} value={region}>
                                {region}
                            </option>
                        ))}
                    </select>
                </div>
            </div>

            <div className="rounded-md border">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Date</TableHead>
                            <TableHead>Campaign</TableHead>
                            <TableHead>Platform</TableHead>
                            <TableHead>Region</TableHead>
                            <TableHead>Impressions</TableHead>
                            <TableHead>Clicks</TableHead>
                            <TableHead>Conversions</TableHead>
                            <TableHead>Spend</TableHead>
                            <TableHead>CTR</TableHead>
                            <TableHead>CPC</TableHead>
                            <TableHead>CPA</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {filteredCampaigns.map((campaign) => (
                            <TableRow key={campaign.id}>
                                <TableCell>
                                    {format(new Date(campaign.date), "MMM d, yyyy")}
                                </TableCell>
                                <TableCell className="font-medium">
                                    {campaign.campaign_name}
                                </TableCell>
                                <TableCell>{campaign.platform}</TableCell>
                                <TableCell>{campaign.region}</TableCell>
                                <TableCell>{campaign.impressions.toLocaleString()}</TableCell>
                                <TableCell>{campaign.clicks.toLocaleString()}</TableCell>
                                <TableCell>{campaign.conversions.toLocaleString()}</TableCell>
                                <TableCell>${campaign.spend.toFixed(2)}</TableCell>
                                <TableCell>{(campaign.ctr * 100).toFixed(2)}%</TableCell>
                                <TableCell>${campaign.cpc.toFixed(2)}</TableCell>
                                <TableCell>${campaign.cpa.toFixed(2)}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>
        </div>
    );
}
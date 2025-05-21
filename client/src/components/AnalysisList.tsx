import type {Analysis} from "@/types";
import {Button} from "@/components/ui/button";
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card";

interface AnalysisListProps {
    analyses: Analysis[];
    onViewDetails: (analysisId: number) => void;
}

export function AnalysisList({analyses, onViewDetails}: AnalysisListProps) {
    const sortedAnalyses = [...analyses].sort((a, b) => {
        const severityOrder = {high: 0, medium: 1, low: 2};
        if (severityOrder[a.severity] !== severityOrder[b.severity]) {
            return severityOrder[a.severity] - severityOrder[b.severity];
        }
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
    });

    const getSeverityColor = (severity: string) => {
        switch (severity) {
            case "high":
                return "bg-red-500";
            case "medium":
                return "bg-yellow-500";
            case "low":
                return "bg-green-500";
            default:
                return "bg-blue-500";
        }
    };

    return (
        <div>
            <h2 className="text-2xl font-bold mb-4">Analysis Results</h2>
            <div className="grid gap-4">
                {sortedAnalyses.length > 0 ? (
                    sortedAnalyses.map((analysis) => (
                        <Card key={analysis.id}>
                            <CardHeader className="pb-2">
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center space-x-2">
                                        <div
                                            className={`h-3 w-3 rounded-full ${getSeverityColor(
                                                analysis.severity
                                            )}`}
                                        />
                                        <CardTitle className="text-lg">{analysis.metric}</CardTitle>
                                    </div>
                                    <span
                                        className="inline-flex h-6 items-center rounded-full bg-primary/10 px-2 text-xs font-medium text-primary">
                    {analysis.severity.toUpperCase()}
                  </span>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <p className="text-sm text-muted-foreground mb-4">
                                    {analysis.description}
                                </p>
                                <div className="flex items-center justify-between">
                                    <div className="flex space-x-4 text-sm text-muted-foreground">
                                        <div>
                                            <span className="font-medium">Value:</span>{" "}
                                            {analysis.value?.toFixed(4) || "N/A"}
                                        </div>
                                        <div>
                                            <span className="font-medium">Expected:</span>{" "}
                                            {analysis.expected_value?.toFixed(4) || "N/A"}
                                        </div>
                                    </div>
                                    <Button size="sm" onClick={() => onViewDetails(analysis.id)}>
                                        View Details
                                    </Button>
                                </div>
                            </CardContent>
                        </Card>
                    ))
                ) : (
                    <Card>
                        <CardContent className="pt-6">
                            <p className="text-muted-foreground">
                                No analysis results found. Click "Run Analysis" to generate
                                insights.
                            </p>
                        </CardContent>
                    </Card>
                )}
            </div>
        </div>
    );
}
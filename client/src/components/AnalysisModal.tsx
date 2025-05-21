import {format} from "date-fns";
import type {AnalysisWithRecommendations} from "@/types";
import {Button} from "@/components/ui/button";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
    DialogFooter,
} from "@/components/ui/dialog";

interface AnalysisModalProps {
    analysis: AnalysisWithRecommendations | null;
    isOpen: boolean;
    onClose: () => void;
    onGenerateRecommendation: (analysisId: number) => void;
}

export function AnalysisModal({
                                  analysis,
                                  isOpen,
                                  onClose,
                                  onGenerateRecommendation,
                              }: AnalysisModalProps) {
    if (!analysis) return null;

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
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-md">
                <DialogHeader>
                    <DialogTitle>Analysis Details</DialogTitle>
                    <DialogDescription>
                        <div className="flex items-center mt-2">
                            <div
                                className={`h-3 w-3 rounded-full ${getSeverityColor(
                                    analysis.severity
                                )}`}
                            />
                            <span className="ml-2 font-medium">
                                {analysis.severity.toUpperCase()} Severity
                            </span>
                        </div>
                    </DialogDescription>
                </DialogHeader>

                <div className="space-y-4">
                    <p className="text-sm">{analysis.description}</p>

                    <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                            <h4 className="font-medium text-muted-foreground">Type</h4>
                            <p>{analysis.type}</p>
                        </div>
                        <div>
                            <h4 className="font-medium text-muted-foreground">Metric</h4>
                            <p>{analysis.metric}</p>
                        </div>
                        <div>
                            <h4 className="font-medium text-muted-foreground">Current Value</h4>
                            <p>{analysis.value?.toFixed(4) || "N/A"}</p>
                        </div>
                        <div>
                            <h4 className="font-medium text-muted-foreground">Expected Value</h4>
                            <p>{analysis.expected_value?.toFixed(4) || "N/A"}</p>
                        </div>
                        {analysis.date_range_start && analysis.date_range_end && (
                            <div className="col-span-2">
                                <h4 className="font-medium text-muted-foreground">Date Range</h4>
                                <p>
                                    {format(new Date(analysis.date_range_start), "MMM d, yyyy")} to{" "}
                                    {format(new Date(analysis.date_range_end), "MMM d, yyyy")}
                                </p>
                            </div>
                        )}
                    </div>

                    <div className="border-t pt-4">
                        <h4 className="font-medium mb-2">AI Recommendations</h4>
                        {analysis.recommendations && analysis.recommendations.length > 0 ? (
                            <div className="max-h-48 overflow-y-auto pr-1">
                                {analysis.recommendations.map((recommendation) => (
                                    <div key={recommendation.id} className="rounded-md bg-muted p-3 text-sm mb-2">
                                        {recommendation.content}
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div>
                                <p className="text-sm text-muted-foreground mb-2">
                                    No recommendations available.
                                </p>
                                <Button
                                    size="sm"
                                    onClick={() => onGenerateRecommendation(analysis.id)}
                                >
                                    Generate Recommendation
                                </Button>
                            </div>
                        )}
                    </div>
                </div>

                <DialogFooter>
                    <Button variant="outline" onClick={onClose}>
                        Close
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}
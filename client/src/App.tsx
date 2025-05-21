import {useState, useEffect} from "react";
import {Header} from "./components/Header";
import {CampaignTable} from "./components/CampaignTable";
import {AnalysisList} from "./components/AnalysisList";
import {AnalysisModal} from "./components/AnalysisModal";
import {getCampaigns, getAnalyses, getAnalysisById, runAnalysis, generateRecommendation} from "./api";
import type {Campaign, Analysis, AnalysisWithRecommendations} from "./types";
import {Alert, AlertDescription} from "@/components/ui/alert";
import {Toaster} from "@/components/ui/sonner";
import {toast} from "sonner"

function App() {
    const [campaigns, setCampaigns] = useState<Campaign[]>([]);
    const [analyses, setAnalyses] = useState<Analysis[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedAnalysis, setSelectedAnalysis] = useState<AnalysisWithRecommendations | null>(null);
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const [campaignsData, analysesData] = await Promise.all([
                    getCampaigns(),
                    getAnalyses()
                ]);
                setCampaigns(campaignsData);
                setAnalyses(analysesData);
            } catch (err) {
                setError('Failed to fetch data');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const handleRunAnalysis = async () => {
        try {
            setLoading(true);
            toast("Running data analysis...");
            await runAnalysis();
            const analysesData = await getAnalyses();
            setAnalyses(analysesData);
            toast("Analysis completed successfully. Email notifications sent for high-severity findings.");
        } catch (err) {
            setError('Failed to run analysis');
            toast("Failed to run analysis.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleViewAnalysisDetails = async (analysisId: number) => {
        try {
            setLoading(true);
            const analysis = await getAnalysisById(analysisId);
            setSelectedAnalysis(analysis);
            setIsModalOpen(true);
        } catch (err) {
            setError('Failed to fetch analysis details');
            toast("Failed to fetch analysis details.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleGenerateRecommendation = async (analysisId: number) => {
        try {
            setLoading(true);
            toast("Generating AI recommendation...");
            await generateRecommendation(analysisId);
            const analysis = await getAnalysisById(analysisId);
            setSelectedAnalysis(analysis);
            toast("AI recommendation generated successfully.");
        } catch (err) {
            setError('Failed to generate recommendation');
            toast("Failed to generate recommendation.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-background py-8 px-8">
            <Header onRunAnalysis={handleRunAnalysis}/>

            <main className="container">
                {loading && (
                    <div className="fixed inset-0 flex items-center justify-center bg-background/80 z-50">
                        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
                    </div>
                )}

                {error && (
                    <Alert variant="destructive" className="mb-6">
                        <AlertDescription>{error}</AlertDescription>
                    </Alert>
                )}

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div className="lg:col-span-2">
                        <h2 className="text-2xl font-bold mb-4">Campaign Data</h2>
                        <CampaignTable campaigns={campaigns}/>
                    </div>

                    <div className="lg:col-span-1">
                        <h2 className="text-2xl font-bold mb-4">Recent Analyses</h2>
                        <div className="max-h-[800px] overflow-y-auto pr-2">
                            <AnalysisList
                                analyses={analyses}
                                onViewDetails={handleViewAnalysisDetails}
                            />
                        </div>
                    </div>
                </div>
            </main>

            <AnalysisModal
                analysis={selectedAnalysis}
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                onGenerateRecommendation={handleGenerateRecommendation}
            />
            <Toaster/>
        </div>
    );
}

export default App;
import { Button } from "@/components/ui/button";

interface HeaderProps {
    onRunAnalysis: () => void;
}

export function Header({ onRunAnalysis }: HeaderProps) {
    return (
        <header className="border-b">
            <div className="container flex h-16 items-center justify-between">
                <h1 className="text-xl font-bold">Marketing Analytics Dashboard</h1>
                <Button onClick={onRunAnalysis}>Run Analysis</Button>
            </div>
        </header>
    );
}
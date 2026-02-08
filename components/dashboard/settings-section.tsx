"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Badge } from "@/components/ui/badge"
import { Shield, ShieldAlert } from "lucide-react"

export function SettingsSection() {
    const [mode, setMode] = useState<"shield" | "guardrail" | "chaos">("shield")

    useEffect(() => {
        const savedMode = localStorage.getItem("securityMode") as "shield" | "guardrail" | "chaos"
        if (savedMode) setMode(savedMode)
    }, [])

    const handleModeChange = (value: "shield" | "guardrail" | "chaos") => {
        setMode(value)
        localStorage.setItem("securityMode", value)
    }

    return (
        <div className="mx-auto">
            <div className="flex items-center justify-between space-x-4 rounded-lg p-4 bg-background border">
                <div className="flex items-center gap-4">
                    <div className="space-y-1">
                        <Label htmlFor="security-mode" className="text-base font-bold">
                            AI Security Mode
                        </Label>
                        <p className="text-sm text-muted-foreground">
                            Choose the level of AI protection and guardrails.
                        </p>
                    </div>
                </div>

                <div className="flex items-center gap-2">

                    <select
                        value={mode}
                        onChange={(e) => handleModeChange(e.target.value as any)}
                        className="h-10 w-[180px] rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    >
                        <option value="shield">AI Shield</option>
                        <option value="guardrail">Standard Guardrail</option>
                        <option value="chaos">Chaos Mode</option>
                    </select>
                </div>
            </div>
        </div>
    )
}

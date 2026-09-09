// tensorx-schnupper.ts — Eigener Modell-Zugang für die Schnuppervorlesung
//
// Nicht der Standardweg: Die Agenten laufen voreingestellt über ein Abo-Modell
// (siehe COUNTING_AGENTS_MODEL in der .env). Dieser Provider ist die
// Ausweichmöglichkeit, wenn dort ein Rate-Limit zuschlägt — und umgekehrt.
//
// pi kennt TensorX bereits global (~/.pi/agent/models.json). Diese Demo meldet
// denselben Endpunkt noch einmal unter eigenem Namen an — mit einem eigenen
// API-Schlüssel aus der projektlokalen `.env`. Zwei Gründe:
//
//   1. Der Vorlesungsschlüssel ist getrennt abrechenbar und lässt sich nach
//      dem Semester zurückziehen, ohne den Alltagszugang anzufassen.
//   2. Die Demo läuft auf jedem Rechner gleich, unabhängig davon, was global
//      in pi eingerichtet ist.
//
// Der Schlüssel steht als `$SCHNUPPER_TENSORX_API_KEY` hier nur als Verweis;
// pi löst ihn bei jeder Anfrage aus der Umgebung auf. Die Startskripte lesen
// dafür die `.env` ein. Im Repo landet der Schlüssel nie.

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.registerProvider("tensorx-schnupper", {
    name: "TensorX (Schnuppervorlesung)",
    baseUrl: "https://api.tensorx.ai/v1",
    apiKey: "$SCHNUPPER_TENSORX_API_KEY",
    api: "openai-completions",
    authHeader: true,
    compat: {
      supportsStore: false,
      supportsDeveloperRole: false,
      supportsUsageInStreaming: true,
      maxTokensField: "max_tokens",
      supportsStrictMode: false,
      supportsLongCacheRetention: false,
    },
    models: [
      {
        id: "qwen/qwen3.8-flash-next",
        name: "Qwen 3.8 Flash Next (Schnuppervorlesung)",
        reasoning: true,
        input: ["text"],
        contextWindow: 262144,
        maxTokens: 32768,
        // Preise pro Million Token — pi rechnet damit die Kosten je Durchlauf
        // aus und zeigt sie im Pane an. Für die Vorlesung ein netter
        // Nebeneffekt: man sieht, was ein Agentenschritt tatsächlich kostet.
        cost: { input: 0.2, output: 0.5, cacheRead: 0.05, cacheWrite: 0 },
        thinkingLevelMap: {
          minimal: "low",
          low: "low",
          medium: "medium",
          high: "xhigh",
          xhigh: "xhigh",
          max: "xhigh",
        },
        compat: {
          supportsReasoningEffort: true,
          thinkingFormat: "chat-template",
          chatTemplateKwargs: { enable_thinking: { $var: "thinking.enabled" } },
        },
      },
    ],
  });
}

# SIH 2025 - Kolam Art Studio Single Flow

```mermaid
flowchart TD
  U[User] --> H[Professional Kolam Studio (React • Port 3000)]
  H --> A{Action}
  A -->|Upload Image| UP[Select/Drop Image → base64]
  A -->|Draw Pattern| DR[Canvas → dataURL]
  A -->|Browse Templates| TP[GET /api/patterns → Templates UI]

  UP --> P[Build JSON Payload]
  DR --> P

  P -->|Basic Analyze| AN[POST /api/analyze]
  P -->|Advanced Analyze| ADV[POST /api/advanced-analysis\nmode: standard/deep • timeout: 10s/22s]
  P -->|Generate Cultural| GC[POST /api/generate-cultural]
  P -->|Generate Festival| GF[POST /api/generate-festival]
  P -->|Generate Template| GG[POST /api/generate]
  H --> HC[GET /api/health]

  subgraph Backend [Flask API • Port 5000]
    R[Router + Validation] --> E{Endpoint}
    AN --> R
    ADV --> R
    GC --> R
    GF --> R
    GG --> R
    HC --> R

    E -->|/api/analyze| BA[Basic Analysis]
    E -->|/api/advanced-analysis| AA[Advanced Image Analysis]
    E -->|/api/generate-cultural| CG[Cultural Generator]
    E -->|/api/generate-festival| FG[Festival Generator]
    E -->|/api/generate| PG[Pattern Generator]
    E -->|/api/patterns| PT[Pattern Templates]
    E -->|/api/health| HL[Health Status]

    BA -->|Analyzer available| MA[KolamAnalyzer → symmetry • complexity • region]
    BA -->|Else| MF[Mock basic analysis]

    AA --> D[Decode base64 → PIL → NumPy]
    D --> DS[Downscale (cv2) • 640/1024 px]
    DS --> PR[Preprocess: gray • blur • threshold • perspective?]
    PR --> HD[Hough Circle Transform (dots)]
    HD --> SK[Skeletonization (lines)]
    SK --> GR[Graph construction (NetworkX)]
    GR --> EU[Eulerian check]
    EU --> SY[Symmetry analysis]
    SY --> CL[Cultural classification]
    CL --> MT[Metrics + Quality score]
    MT --> TB{Time budget exceeded?]
    TB -->|Yes| FBF[Fallback dynamic advanced mock]
    TB -->|No| RES1[Advanced analysis JSON]

    CG --> CGP[Grid + regional rules + colors + metadata]
    FG --> FGP[Grid + festival rules + colors + symbolism]
    PG --> PGP[Grid + symmetry + paths + colors]

    RES1 --> RESP
    FBF --> RESP
    MA --> RESP
    MF --> RESP
    CGP --> RESP
    FGP --> RESP
    PGP --> RESP
    PT --> RESP
    HL --> RESP

    RESP[JSON response • processing_steps • messages]
  end

  RESP --> UIU[Frontend state update • toasts • cards]
  UIU --> DRAW[Canvas render • Results panels]
  DRAW --> EXP[Export PNG/SVG/JSON]
  UIU --> ERR{Error?}
  ERR -->|Timeout| TOH[Show timeout tip • suggest retry]
  ERR -->|HTTP 500| FB[Show fallback used]
  ERR -->|Network| NET[Show connection error]
```

"""Module collecting constants and ENV variables"""

import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.environ["PROJECT_ID"]
PROJECT_ENV = os.environ["PROJECT_ENV"]
GCS_BUCKET = f"cdp_gcs_coros_ew1_{PROJECT_ENV.lower()}"

SECRET_KEY_SECRET_ID = f"cdp_srt_crypto_secret_key_{PROJECT_ENV.lower()}"
API_KEY_SECRET_ID = f"cdp_srt_crypto_api_key_{PROJECT_ENV.lower()}"
QUOTE_ASSET = "USDT"

COINS_TO_TRADE= {
    "DEV": ["BTC", "ETH", "BNB", "NEO", "LTC", "QTUM", 
            "ADA", "XRP", "EOS", "TUSD", "IOTA", "XLM"],
    "PRD": ["BTC", "ETH", "BNB", "NEO", "LTC", "QTUM", 
            "ADA", "XRP", "EOS", "TUSD", "IOTA", "XLM", 
            "ONT", "TRX", "ETC", "ICX", "VET", "USDC", 
            "LINK", "ONG", "HOT", "ZIL", "ZRX", "FET", 
            "BAT", "ZEC", "IOST", "CELR", "DASH", "THETA", 
            "ENJ", "ATOM", "TFUEL", "ONE", "ALGO", "DOGE", 
            "DUSK", "ANKR", "WIN", "COS", "MTL", "DENT", "WAN", 
            "FUN", "CVC", "CHZ", "BAND", "XTZ", "RVN", "HBAR", 
            "NKN", "STX", "KAVA", "ARPA", "IOTX", "RLC", "BCH", 
            "FTT", "OGN", "LSK", "BNT", "LTO", "MBL", "COTI", 
            "STPT", "DATA", "SOL", "CTSI", "HIVE", "CHR", "ARDR", 
            "MDT", "KNC", "LRC", "COMP", "SC", "ZEN", "SNX", 
            "VTHO", "DGB", "SXP", "MKR", "DCR", "STORJ", 
            "MANA", "YFI", "KMD", "JST", "CRV", "SAND", 
            "NMR", "DOT", "LUNA", "RSR", "PAXG", "TRB", 
            "SUSHI", "KSM", "EGLD", "DIA", "RUNE", "FIO", 
            "UMA", "BEL", "UNI", "OXT", "SUN", "AVAX", "FLM", 
            "UTK", "XVS", "ALPHA", "AAVE", "NEAR", "FIL", 
            "INJ", "AUDIO", "CTK", "AXS", "STRAX", "ROSE", 
            "AVA", "SKL", "GRT", "JUV", "PSG", "1INCH", "OG", 
            "ATM", "ASR", "CELO", "RIF", "TRU", "CKB", 
            "TWT", "SFP", "DODO", "CAKE", "ACM", "FIS", 
            "OM", "POND", "DEGO", "ALICE", "PERP", "SUPER", 
            "CFX", "TKO", "PUNDIX", "TLM", "BAR", "FORTH", 
            "BAKE", "SLP", "SHIB", "ICP", "AR", "MASK", 
            "LPT", "XVG", "ATA", "GTC", "PHA", "MLN", "DEXE", 
            "C98", "QNT", "FLOW", "MINA", "RAY", "FARM", 
            "QUICK", "MBOX", "REQ", "GHST", "WAXP", "GNO", 
            "XEC", "DYDX", "IDEX", "USDP", "GALA", "ILV", 
            "YGG", "SYS", "DF", "FIDA", "AGLD", "RAD", 
            "RARE", "LAZIO", "CHESS", "ADX", "AUCTION", 
            "MOVR", "CITY", "ENS", "QI", "PORTO", "POWR", 
            "JASMY", "AMP", "PYR", "ALCX", "SANTOS", "BICO", 
            "FLUX", "FXS", "VOXEL", "HIGH", "CVX", 
            "PEOPLE", "SPELL", "JOE", "ACH", "IMX", "GLMR", 
            "LOKA", "SCRT", "API3", "BTTC", "ACA", "XNO", 
            "WOO", "ALPINE", "T", "ASTR", "GMT", "KDA", "APE", 
            "BSW", "BIFI", "STEEM", "NEXO", "REI", "LDO", "OP", 
            "LEVER", "STG", "LUNC", "GMX", "POLYX", "APT", 
            "OSMO", "HFT", "PHB", "HOOK", "MAGIC", "HIFI", 
            "RPL", "GNS", "SYN", "SSV", "LQTY", "USTC", 
            "GAS", "GLM", "PROM", "QKC", "ID", "ARB", "RDNT", 
            "WBTC", "EDU", "SUI", "PEPE", "FLOKI", "MAV", 
            "PENDLE", "ARKM", "WBETH", "WLD", "FDUSD", "SEI", 
            "CYBER", "ARK", "IQ", "NTRN", "TIA", "MEME", 
            "ORDI", "BEAMX", "PIVX", "VIC", "BLUR", "VANRY", 
            "AEUR", "JTO", "1000SATS", "BONK", "ACE", "NFP", 
            "AI", "XAI", "MANTA", "ALT", "JUP", "PYTH", "RONIN", 
            "DYM", "PIXEL", "STRK", "PORTAL", "AXL", "WIF", 
            "METIS", "AEVO", "BOME", "ETHFI", "ENA", "W", 
            "TNSR", "SAGA", "TAO", "OMNI", "REZ", "BB", 
            "NOT", "IO", "ZK", "LISTA", "ZRO", "G", 
            "BANANA", "RENDER", "TON", "DOGS", "EURI", 
            "SLF", "POL", "NEIRO", "TURBO", "1MBABYDOGE", 
            "CATI", "HMSTR", "EIGEN", "SCR", "BNSOL", 
            "LUMIA", "KAIA", "COW", "CETUS", "PNUT", "ACT", 
            "USUAL", "THE", "ACX", "ORCA", "MOVE", "ME", "VELODROME", 
            "VANA", "1000CAT", "PENGU", "BIO", "D", "AIXBT", "CGPT", 
            "COOKIE", "S", "SOLV", "TRUMP", "ANIME", "BERA", "1000CHEEMS", 
            "TST", "LAYER", "HEI", "KAITO", "SHELL", "RED", "GPS", "EPIC", 
            "BMT", "FORM", "XUSD", "NIL", "PARTI", "MUBARAK", "TUT", 
            "BROCCOLI714", "BANANAS31", "GUN", "BABY", "ONDO", 
            "BIGTIME", "VIRTUAL", "KERNEL", "WCT", "HYPER", "INIT", 
            "SIGN", "STO", "SYRUP", "KMNO", "SXT", "NXPC"]
}

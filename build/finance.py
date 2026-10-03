"""Finance questions.

Each question is written in our own words. `src` lists the rows of the source
reports it was drawn from (a file letter plus the spreadsheet row number);
build.py checks those against finance_sources.json and that every row is
accounted for.

Answer kinds:
- open:   no single right answer; Check shows key points to compare against
- number: Check compares to `value` within a tolerance; the build recomputes
          `value` from `solve` and checks it matches what we wrote
- choice: pick one option
- expr:   build an arithmetic expression (e.g. make 25 from 2, 4, 6, 8)
"""
import math

FIN = []

# Report rows deliberately left out, with the reason.
EXCLUDED = {
    "G25": "only links to documents described as internal and not for distribution; not used",
    "J36": "general impressions only, no specific questions",
}
# Rows with only behavioral questions, which the site doesn't include.
EXCLUDED.update({row: "behavioral questions only" for row in
                 "G3 G4 G5 G9 G12 G15 G16 G20 G24 G26 G28 J3 J13 J14 J21 J22 J44 J45 J46 U4".split()})


def fq(id, cat, title, text, src, key=None, answer=None, explain=None):
    FIN.append(dict(id=id, cat=cat, title=title, text=text, src=src.split(),
                    key=key or [], answer=answer or {"type": "open"}, explain=explain or []))


def num(solve, value, unit="", tol=0.01):
    """`value` is what we expect; `solve()` recomputes it (checked by the build)."""
    return {"type": "number", "solve": solve, "value": value, "unit": unit, "tol": tol}


def choice(options, correct):
    return {"type": "choice", "options": options, "correct": correct}


def expr(numbers, target, reference):
    return {"type": "expr", "numbers": numbers, "target": target, "reference": reference}


# =============================================================================
# Technical: valuation
# =============================================================================

fq("valuation-methods", "technical", "Valuation Methodologies",
   "What are the main ways to value a company, and which one usually gives the highest value? Why?",
   "U3 U6 U7 U9 U10 U11 U12 U13 U14 G2 G11 G19 G21 G23 J2 J5 J17 J18 J23 J26 J29 J32 J41 J42 J48 J49 J55 J59 J60", key=[
    "Comparable companies (trading comps): value from multiples of similar public companies.",
    "Precedent transactions: value from multiples paid in past acquisitions of similar companies.",
    "Discounted cash flow (DCF): present value of projected free cash flows plus a terminal value.",
    "Precedents usually come out highest because they include a control premium (and often synergies).",
    "A DCF can be highest or lowest depending on its assumptions; LBO analysis often sets a floor.",
    "Mention pros and cons: comps reflect today's market, precedents may be stale, a DCF is assumption-heavy.",
])

fq("dcf-walkthrough", "technical", "Walk Me Through a DCF",
   "Walk me through a discounted cash flow analysis from start to finish.",
   "U3 U5 U6 U7 U17 G23 J9 J25", key=[
    "Project the company's unlevered free cash flow for about 5-10 years.",
    "Pick a discount rate, normally WACC, which reflects the risk to all capital providers.",
    "Calculate terminal value with the perpetuity growth method or an exit multiple.",
    "Discount the cash flows and terminal value back to today and add them to get enterprise value.",
    "Bridge to equity value (subtract net debt and other claims) and divide by diluted shares for a per-share value.",
    "Finish with sensitivity tables on WACC and the growth rate or exit multiple.",
])

fq("unlevered-fcf", "technical", "Getting to Unlevered Free Cash Flow",
   "Without using numbers, walk me through the line items that take you from revenue to unlevered free cash flow.",
   "U17 J7 J18 J26 J48 J57 J60", key=[
    "Start with revenue and subtract operating costs to reach EBIT.",
    "Subtract taxes on EBIT (EBIT × (1 − tax rate)) to get NOPAT; interest is ignored because it's unlevered.",
    "Add back non-cash charges such as depreciation and amortization.",
    "Subtract capital expenditures.",
    "Subtract the increase in net working capital (or add a decrease).",
    "The result goes to both debt and equity holders, so it's discounted at WACC.",
])

fq("terminal-value", "technical", "Terminal Value",
   "What are the two ways to calculate terminal value in a DCF? How high can the long-term growth rate reasonably be?",
   "U6 G6 J5 J17 J18 J23 J32 J41 J49 J60", key=[
    "Perpetuity growth (Gordon growth): TV = FCF in the final year × (1 + g) ÷ (WACC − g).",
    "Exit multiple: TV = final-year EBITDA (or another metric) × a multiple from comps or precedents.",
    "The growth rate should stay at or below long-run GDP growth or inflation, roughly 2-3%.",
    "g must be below WACC, or the formula breaks down.",
    "Cross-check the two: the implied multiple from the growth method should look reasonable, and vice versa.",
])

fq("wacc", "technical", "Calculating WACC",
   "How do you calculate a company's weighted average cost of capital, and what happens to it as the company takes on more debt?",
   "U7 G2 J8 J9 J18 J34 J59 J60", key=[
    "WACC = E/(D+E) × cost of equity + D/(D+E) × cost of debt × (1 − tax rate).",
    "Cost of equity usually comes from CAPM: risk-free rate + beta × equity risk premium.",
    "Cost of debt comes from the company's borrowing rate or bond yields, after tax because interest is deductible.",
    "Adding debt first lowers WACC (debt is cheaper and tax-deductible).",
    "Past a point, distress risk raises both the cost of debt and equity, so WACC rises again: a U-shaped curve.",
    "A distressed company has a much higher cost of capital, not a lower risk-free rate.",
])

fq("beta", "technical", "What Is Beta?",
   "In the context of an investment, what is beta? Give an example of a high-beta and a low-beta company.",
   "U7 G2 J7 J18 J57 J59 J60", key=[
    "Beta measures how much a stock moves relative to the overall market (the market has a beta of 1).",
    "It captures systematic risk that can't be diversified away and feeds into CAPM's cost of equity.",
    "High beta (above 1): cyclical or high-growth businesses, such as tech, airlines or luxury goods.",
    "Low beta (below 1): stable demand, such as utilities, consumer staples or healthcare.",
    "Leverage raises equity beta; you unlever comps' betas and relever at the target's capital structure.",
])

fq("small-business-valuation", "technical", "Valuing a Small Local Business",
   "A local business, such as a laundromat, coffee shop or taco truck, asks you to help it sell. How would you value it?",
   "G30 J4 J12 J18 J20 J27 J28 J33 J54 J60", key=[
    "Start with its cash flows: revenue, operating costs, owner's salary, rent, and what's left over.",
    "Use multiples from recent sales of similar small businesses (often a multiple of cash flow or EBITDA).",
    "A simple DCF of expected cash flows, using a high discount rate for a small, risky business.",
    "Value the assets (equipment, lease, location) as a floor.",
    "Consider who would buy it: an individual owner, a competitor or a chain, and what each would pay.",
    "For a chain, strategic buyers or PE roll-ups may pay more because of synergies.",
])

fq("no-earnings-valuation", "technical", "Valuing a Company With No Earnings",
   "How would you value a company that doesn't make a profit yet, or an early-stage startup with little financial history?",
   "G23 G29 J2 J33", key=[
    "Use revenue or other top-line multiples (EV/Revenue) instead of earnings multiples.",
    "Use operating metrics for the industry: users, subscribers, bookings, gross merchandise value.",
    "A DCF with a long projection period until the business matures, at a high discount rate.",
    "Look at recent funding rounds and comparable private transactions.",
    "For very early companies, think about team, market size and the probability of success.",
])

fq("high-growth-dcf", "technical", "Modeling a Fast-Growing Company",
   "A company grew revenue 50% last year. What do you need to think about in your DCF? How long should the projection period be, and what matters most in today's markets when you build valuation materials?",
   "G11 G30", key=[
    "50% growth isn't sustainable, so taper growth gradually toward a steady state.",
    "Use a longer projection period (often 10 years or more) so the business can mature before terminal value.",
    "Check that margins, reinvestment (capex, working capital) and dilution are consistent with that growth.",
    "Terminal value will be a large share of the value; sensitize it carefully.",
    "In current markets, think about the rate environment's effect on discount rates and where peers trade.",
])

fq("projections", "technical", "Building and Checking Projections",
   "A client hands you an operating model, or you have to build projections for a manufacturing company. What do you look at first, and how do you set your assumptions?",
   "U5 G30 J25", key=[
    "Check historicals first: do the numbers tie to the financial statements?",
    "Make sure the main drivers are explicit: volume, price, capacity, input costs, margins.",
    "Compare growth and margins with history, peers and industry outlook; flag aggressive assumptions.",
    "For manufacturing, focus on capacity utilization, raw material costs, capex and working capital.",
    "Build bull, base and bear cases rather than one point estimate.",
])

fq("oil-major-vs-growth", "technical", "Comparing Two Financial Profiles",
   "Compare the financial profiles of a large oil company and a fast-growing electric car maker. What differences drive how the market values them?",
   "J18 J35 J50 J60", key=[
    "Growth: the oil major grows slowly with commodity prices; the high-growth company is valued on future growth.",
    "Cash flow and payouts: the oil major returns cash through dividends and buybacks; the growth company reinvests.",
    "Multiples: the growth company trades at much higher P/E and EV/EBITDA multiples.",
    "Risk drivers: commodity price cycles versus execution and competition risk.",
    "Capital intensity and margins differ, and so do beta and cost of capital.",
])

fq("goldmine-valuation", "technical", "Valuing a Finite Resource",
   "How would you value a gold mine, or any asset that runs out, with a DCF? Would it have a terminal value?",
   "J8 J28", key=[
    "Project cash flows over the mine's life from reserves, production rate, gold price and extraction costs.",
    "There's usually no perpetual terminal value because the resource is depleted.",
    "Include closure and cleanup costs at the end.",
    "Sensitize heavily to the commodity price, the biggest driver.",
])

fq("conglomerate", "technical", "Valuing a Conglomerate",
   "Which valuation approach suits a large conglomerate with several unrelated businesses?",
   "J55", key=[
    "A sum-of-the-parts analysis: value each segment separately with its own peers and multiples.",
    "Add the segment values, then subtract net debt and unallocated corporate costs.",
    "Conglomerates often trade at a discount to that sum, which can motivate spin-offs.",
])

fq("ebitda-limits", "technical", "Limits of EBITDA",
   "Why can EBITDA be a misleading metric? When might you look at EBITDAR instead, and why might a DCF not add back stock-based compensation?",
   "J26 J30", key=[
    "EBITDA ignores capex, so capital-intensive businesses look better than their cash flow.",
    "It also ignores working capital changes, interest and taxes.",
    "Companies can define 'adjusted EBITDA' generously.",
    "EBITDAR adds back rent, which makes companies that lease versus own their property comparable (common in gaming, retail and airlines).",
    "Stock-based compensation is a real cost that dilutes shareholders; not adding it back avoids overstating cash flow.",
])

fq("ev-multiples-cash-flow", "technical", "Matching Multiples and Cash Flows",
   "Name one unlevered (enterprise value) multiple and one levered (equity value) multiple. Which free cash flow goes with enterprise value?",
   "G6 J26", key=[
    "Enterprise value multiples: EV/EBITDA, EV/Revenue, EV/EBIT.",
    "Equity value multiples: P/E, Price/Book, Equity Value/Levered FCF.",
    "Enterprise value pairs with unlevered FCF (before interest), since both belong to all capital providers.",
    "Equity value pairs with levered FCF (after interest), which belongs only to shareholders.",
])

fq("equity-to-enterprise", "technical", "Equity Value to Enterprise Value",
   "Walk me from equity value to enterprise value. Can equity value ever be negative? Should a company's liquid investments count in enterprise value? How does minority interest fit in?",
   "J12 J25", key=[
    "EV = equity value + debt + preferred stock + noncontrolling (minority) interest − cash and equivalents.",
    "Liquid, non-operating investments are treated like cash and subtracted.",
    "Minority interest is added because the consolidated EBITDA includes 100% of subsidiaries you don't fully own.",
    "Market equity value can't be negative (share prices can't be), but book equity can be.",
])

fq("fig-valuation", "technical", "Valuing a Bank",
   "How do you value and project cash flow for a financial institution such as a bank? Which methods are most common in FIG?",
   "J48", key=[
    "Debt is part of a bank's operations, so EV and EBITDA don't really apply.",
    "Use equity-based multiples: P/E, Price/Book and Price/Tangible Book Value.",
    "Use a dividend discount model instead of an unlevered DCF.",
    "Key drivers: net interest margin, loan growth, credit losses and regulatory capital ratios.",
])

# =============================================================================
# Technical: accounting
# =============================================================================

fq("three-statements", "technical", "Linking the Three Statements",
   "How do the income statement, balance sheet and cash flow statement connect? How would you build the cash flow statement from the other two?",
   "J2 J48 J52", key=[
    "Net income from the income statement is the first line of the cash flow statement.",
    "The cash flow statement adds back non-cash items and adjusts for working capital changes taken from the balance sheet.",
    "Investing (capex) and financing (debt, equity, dividends) activities come from balance sheet changes.",
    "Ending cash from the cash flow statement becomes cash on the balance sheet.",
    "Net income, less dividends, flows into retained earnings in shareholders' equity.",
])

fq("equipment-purchase", "technical", "Buying Equipment",
   "A company buys a piece of equipment. Walk me through the effect on the three financial statements, at purchase and over time.",
   "J6 J18 J19 J53 J60", key=[
    "At purchase: no income statement effect.",
    "Cash flow statement: capex in investing activities reduces cash.",
    "Balance sheet: cash goes down and PP&E goes up by the same amount, so it balances.",
    "Over time, depreciation hits the income statement, is added back on the cash flow statement, and reduces PP&E.",
    "If it's financed with debt, debt rises and financing cash flow offsets the cash outflow.",
])

fq("depreciation-change", "technical", "Depreciation Goes Up by $10",
   "Depreciation increases by $10 and the tax rate is 25%. By how much does the company's cash change? (Give a number; then think through all three statements.)",
   "U3 G19 J18 J58 J60",
   answer=num(lambda: 10 * 0.25, 2.5, unit="$"), explain=[
    "Income statement: pre-tax income falls $10, taxes fall $2.50, net income falls $7.50.",
    "Cash flow statement: net income −$7.50, add back depreciation +$10, so cash is up $2.50.",
    "Balance sheet: cash +$2.50, PP&E −$10, so assets are −$7.50; retained earnings −$7.50, so it balances.",
    "The cash gain is the tax shield: $10 × 25% = $2.50.",
])

fq("receivables", "technical", "Accounts Receivable and Other Working Capital",
   "What is accounts receivable? How do changes in receivables, payables and deferred revenue flow through the statements? How could a company use receivables to shift reported earnings?",
   "J2 J26 J28 J48", key=[
    "Accounts receivable is revenue earned but not yet collected in cash.",
    "An increase in receivables reduces operating cash flow; an increase in payables or deferred revenue increases it.",
    "Each change shows up on the balance sheet and in the working capital section of the cash flow statement.",
    "Aggressive revenue recognition (booking sales early, loose credit terms) inflates receivables and earnings.",
    "Changes in reserves for doubtful accounts can also move earnings.",
])

fq("ar-cash", "technical", "Receivables Go Up by $10",
   "With nothing else changing, accounts receivable rises by $10. By how much does cash change? (Use a minus sign for a decrease.)",
   "J26 J28",
   answer=num(lambda: -10, -10, unit="$"), explain=[
    "A higher receivables balance means $10 of sales hasn't been collected in cash.",
    "On the cash flow statement, the increase in a working capital asset is subtracted: −$10.",
    "Balance sheet: receivables +$10 and cash −$10, so total assets don't change.",
])

fq("lifo-fifo", "technical", "LIFO vs FIFO",
   "What's the difference between LIFO and FIFO inventory accounting, and how does the choice affect profit when prices are rising?",
   "J2 J28 J55", key=[
    "FIFO (first in, first out) expenses the oldest inventory costs first; LIFO expenses the newest first.",
    "When prices rise, LIFO gives higher cost of goods sold, lower profit and lower taxes.",
    "FIFO gives lower COGS, higher profit and a balance sheet inventory value closer to current cost.",
    "LIFO isn't allowed under IFRS, only US GAAP.",
])

# =============================================================================
# Technical: M&A, LBO, capital structure
# =============================================================================

fq("why-acquire", "technical", "Why Companies Merge",
   "Why do companies acquire or merge with other companies? What factors drive the decision?",
   "G2 G10 G18 G19 J12 J55 J62", key=[
    "Growth: enter new markets, products or customers faster than building them.",
    "Synergies: cost savings and cross-selling opportunities.",
    "Buying technology, talent or intellectual property.",
    "Consolidation for scale and pricing power, or to remove a competitor.",
    "Diversification, tax benefits, or deploying excess cash when organic growth slows.",
])

fq("synergies", "technical", "Types of Synergies",
   "What are the two main types of synergies in a merger? Give an example of each.",
   "J6 J18 J19 J60", key=[
    "Cost synergies: savings from combining operations, such as closing duplicate offices, cutting overlapping staff, or buying supplies at scale.",
    "Revenue synergies: extra sales, such as cross-selling products to each other's customers or entering new regions.",
    "Cost synergies are more within management's control and are valued more highly.",
])

fq("cost-vs-revenue-synergy", "technical", "Which Synergy Is Worth More?",
   "Which is usually worth more to an acquirer: $1 of cost synergies or $1 of revenue synergies?",
   "J4 J18 J54 J60",
   answer=choice(["Cost synergies", "Revenue synergies", "They're worth the same"], "Cost synergies"), explain=[
    "A $1 cost saving goes almost straight to profit, while $1 of extra revenue only adds its margin.",
    "Cost savings are more within the company's control and more likely to happen.",
    "Investors and buyers therefore give cost synergies more credit when pricing a deal.",
])

fq("acquisition-premium", "technical", "Paying Above Market Price",
   "A public company trades at $30 per share. Why would a buyer pay $40? And why might two identical companies sell at different multiples?",
   "G30 J2 J18 J34 J60", key=[
    "A control premium: the buyer gets to run the company and its cash flows.",
    "Synergies the buyer expects to capture are worth more to it than to the market.",
    "Competition in an auction pushes the price up.",
    "The buyer may see undervaluation, strategic value, or defensive reasons (keeping it from a rival).",
    "Identical companies can sell at different multiples because of market conditions, timing, buyer type, the competitiveness of the process, and deal terms.",
])

fq("deal-funding", "technical", "Funding an Acquisition: Debt or Equity",
   "A company wants to buy another for cash. Where could the money come from? When is debt better, and when is issuing equity better?",
   "J2 J9 J10 J18 J30 J51 J58 J60", key=[
    "Sources: cash on hand, new debt, new equity, or a mix.",
    "Debt is cheaper and keeps ownership, but adds interest costs and risk; it fits stable cash flows, low rates and low current leverage.",
    "Equity adds no interest or repayment, but dilutes shareholders; it fits a high share price, high leverage, or uncertain cash flows.",
    "Rating agencies, covenants and the target's own cash flow all affect the mix.",
])

fq("excess-cash", "technical", "What to Do With Excess Cash",
   "As CFO, you have excess cash. What could you do with it, and when would you recommend each option?",
   "G8 J10 J16 J18 J60", key=[
    "Reinvest in the business (capex, R&D) if returns beat the cost of capital.",
    "Acquire another company when there's a good strategic fit at a fair price.",
    "Pay down debt if leverage is high or rates are high.",
    "Return cash with dividends (steady, long-term) or buybacks (flexible, signals undervaluation).",
    "Hold some as a buffer when the outlook is uncertain.",
])

fq("debt-vs-equity-investor", "technical", "Debt vs Equity Investors",
   "How does a debt (credit) investor think differently from an equity investor?",
   "G8 J26 J48", key=[
    "Debt investors have capped upside (interest and principal), so they focus on downside protection.",
    "They care about cash flow stability, leverage, coverage ratios, collateral and covenants.",
    "Equity investors have unlimited upside and care most about growth and returns.",
    "Equity holders are paid last if the company fails, so they accept more risk for higher potential returns.",
])

fq("creditworthiness", "technical", "Judging Creditworthiness",
   "What makes a company a good credit investment? What would a bank look at before lending, for example to a university or other non-profit?",
   "U5 U7 J63", key=[
    "Stable, predictable cash flow to cover interest and principal.",
    "Leverage (debt / EBITDA) and interest coverage (EBITDA / interest).",
    "Collateral, covenants and where the debt sits in the capital structure.",
    "Industry risk, competitive position and management quality.",
    "For a university: enrollment trends, tuition dependence, endowment size, donations, and existing debt.",
])

fq("lbo-candidate", "technical", "A Good LBO Candidate",
   "What makes a company a good candidate for a leveraged buyout?",
   "G2 G11 U8 J30", key=[
    "Stable, predictable cash flow to service the debt.",
    "Low existing debt and a strong asset base to borrow against.",
    "Low capex needs and opportunities to cut costs or improve operations.",
    "A strong market position and good management.",
    "A clear exit route through a sale or IPO, at a reasonable entry price.",
])

fq("lbo-structure", "technical", "LBO Model Basics",
   "Without using numbers, walk me through an LBO: sources and uses, the line items down to free cash flow, and what drives returns.",
   "J18 J25 J35 J50 J56 J60", key=[
    "Uses: purchase price for the equity, refinancing existing debt, and fees.",
    "Sources: new debt (often several tranches) and the sponsor's equity.",
    "From revenue to EBITDA, minus interest, taxes, capex and working capital changes, to get levered FCF available to pay down debt.",
    "At exit, value the business with a multiple, subtract remaining debt, and compare equity proceeds to equity invested.",
    "Returns come from EBITDA growth, debt paydown, and multiple expansion.",
])

fq("merger-model", "technical", "How a Merger Model Works",
   "How does a merger model (accretion/dilution analysis) work? If a public company buys a public target entirely with cash, how do you get to pro forma net income? What models get built during an M&A deal?",
   "J12 J25 J55 J56", key=[
    "Combine the buyer's and target's net income (or EBIT, then taxes).",
    "With cash: subtract foregone interest on the cash used, after tax; with new debt, subtract after-tax interest.",
    "With stock: add the new shares issued to the share count.",
    "Add synergies and subtract new amortization of acquired intangibles.",
    "Pro forma EPS vs the buyer's standalone EPS shows accretion or dilution.",
    "Other models in a deal: valuation (DCF, comps), LBO for a sponsor's view, and contribution analysis.",
])

fq("sell-side-process", "technical", "The M&A Process",
   "Walk me through a sell-side M&A process. How does a buy-side process differ?",
   "J2 J25 U5", key=[
    "Prepare: valuation, a teaser and a confidential information memorandum (CIM), and a buyer list.",
    "First round: buyers sign NDAs, receive the CIM, and submit indications of interest.",
    "Second round: selected buyers get management presentations and data room access, then submit final bids.",
    "Negotiate the purchase agreement with the winner, then sign, get approvals and close.",
    "Buy-side: help a client find targets, value them, structure the offer and run diligence.",
])

fq("buyer-preferences", "technical", "Strategic Buyer vs Private Equity",
   "Who usually pays more for a company: a strategic buyer or a private equity firm? When could PE pay more? Why might management and investors each prefer one or the other?",
   "U18 J8 J12 J62", key=[
    "Strategics usually pay more because they can capture synergies.",
    "PE can pay more when it's building a platform and merging the target into a portfolio company (an add-on with synergies).",
    "Shareholders often prefer the highest price and certainty of closing.",
    "Management may prefer PE: they often keep their jobs and get equity.",
    "A strategic may integrate and cut roles; PE adds leverage and a planned exit.",
])

fq("strategic-vs-pe-choice", "technical", "Who Pays More?",
   "In general, which kind of buyer can afford to pay a higher price for a company?",
   "J8 J62",
   answer=choice(["A strategic buyer", "A private equity firm"], "A strategic buyer"), explain=[
    "A strategic buyer can count on synergies (cost savings, cross-selling) that a standalone PE owner can't.",
    "PE firms are limited by the debt they can raise and their target return (often around 20-25% IRR).",
    "The exception: PE firms buying an add-on for an existing portfolio company can capture synergies too.",
])

fq("price-vs-volume", "technical", "Price or Volume?",
   "A business can grow revenue 10% either by raising prices 10% or by selling 10% more units. Which usually adds more profit?",
   "J12 J28 J30",
   answer=choice(["Raise prices", "Sell more units"], "Raise prices"), explain=[
    "A price increase adds revenue with no extra costs, so almost all of it is profit.",
    "Selling more units also raises variable costs (materials, labor, shipping).",
    "The catch: higher prices can cost customers if demand is price-sensitive, so mention elasticity.",
])

fq("pe-accretion-cheap-buyer", "technical", "Accretive or Dilutive? (All-Stock, Lower P/E Buyer)",
   "A buyer with a P/E of 10x acquires a seller with a P/E of 15x, paying entirely in stock. Is the deal accretive or dilutive to the buyer's EPS (ignoring synergies)?",
   "U17 J9",
   answer=choice(["Accretive", "Dilutive"], "Dilutive"), explain=[
    "In an all-stock deal, the buyer's cost of acquisition is its earnings yield: 1 ÷ 10x = 10%.",
    "The seller's earnings yield is 1 ÷ 15x = 6.7%.",
    "The buyer gives up more earnings per share issued than it gets back, so EPS falls: dilutive.",
    "Rule of thumb: buying a higher-P/E company with lower-P/E stock is dilutive.",
])

fq("pe-accretion-rich-buyer", "technical", "Accretive or Dilutive? (All-Stock, Higher P/E Buyer)",
   "Company A trades at 25x earnings and buys Company B, which trades at 10x, paying entirely in stock. Accretive or dilutive to A's EPS?",
   "U6 J55 J59",
   answer=choice(["Accretive", "Dilutive"], "Accretive"), explain=[
    "A's cost of using its stock is its earnings yield: 1 ÷ 25x = 4%.",
    "B's earnings yield is 1 ÷ 10x = 10%.",
    "A buys more earnings than it gives up, so EPS rises: accretive.",
])

fq("mixed-consideration", "technical", "Accretive or Dilutive? (Half Cash, Half Stock)",
   "The buyer's P/E is 10x and the seller's is 15x. The buyer pays 50% in stock and 50% in cash; the cash earns 4% pre-tax interest and the tax rate is 25%. What is the buyer's weighted cost of acquisition, in %? (Compare it with the seller's 6.7% earnings yield.)",
   "U17 J55 J59",
   answer=num(lambda: 0.5 * (1 / 10) * 100 + 0.5 * 4 * (1 - 0.25), 6.5, unit="%"), explain=[
    "Cost of stock = buyer's earnings yield = 1 ÷ 10x = 10%.",
    "Cost of cash = foregone after-tax interest = 4% × (1 − 25%) = 3%.",
    "Weighted cost = 50% × 10% + 50% × 3% = 6.5%.",
    "The seller's earnings yield is 1 ÷ 15x ≈ 6.7%, which is above 6.5%, so the deal is (slightly) accretive.",
    "Same P/Es as the all-stock version, but cheaper funding flips it from dilutive to accretive.",
])

fq("lbo-irr", "technical", "LBO Returns",
   "You buy a company at 10x EBITDA of $100m, funded with 7x leverage and the rest in equity. Over 5 years you pay down $100m of debt, and you sell at 15x EBITDA, which is still $100m. What is your IRR, in %?",
   "G2",
   answer=num(lambda: ((15 * 100 - (7 * 100 - 100)) / (10 * 100 - 7 * 100)) ** (1 / 5) * 100 - 100, 24.57, unit="%", tol=0.02), explain=[
    "Entry: EV = 10 × $100m = $1,000m; debt = 7 × $100m = $700m; equity = $300m.",
    "Exit: EV = 15 × $100m = $1,500m; debt = $700m − $100m = $600m; equity = $900m.",
    "Multiple of money = $900m ÷ $300m = 3.0x over 5 years.",
    "IRR = 3.0^(1/5) − 1 ≈ 24.6%. (Rule of thumb: 3x in 5 years is about 25%.)",
])

fq("lbo-exit-multiple", "technical", "Required Exit Multiple",
   "A company has $1bn revenue and a 10% EBITDA margin, and is bought at 10x EBITDA with 5x leverage. EBITDA then triples, and the buyer wants a 2.0x return on equity. Assuming the debt stays the same, what EV/EBITDA multiple must it sell at?",
   "U18",
   answer=num(lambda: (2 * (10 * 100 - 5 * 100) + 5 * 100) / (3 * 100), 5.0, unit="x"), explain=[
    "EBITDA = 10% × $1,000m = $100m. Entry EV = 10 × $100m = $1,000m.",
    "Debt = 5 × $100m = $500m, so equity invested = $500m.",
    "A 2.0x return needs $1,000m of equity at exit; plus $500m of debt, exit EV = $1,500m.",
    "New EBITDA = 3 × $100m = $300m, so exit multiple = $1,500m ÷ $300m = 5.0x.",
])

fq("lbo-exit-equity", "technical", "Equity Needed for a 3x Return",
   "A company with $10 of EBITDA is bought at 5x EBITDA using 3x leverage. To earn a 3.0x multiple of money, how much equity value does the sponsor need at exit?",
   "U18",
   answer=num(lambda: 3 * (5 * 10 - 3 * 10), 60, unit="$"), explain=[
    "Entry EV = 5 × $10 = $50; debt = 3 × $10 = $30; equity invested = $20.",
    "A 3.0x return means exit equity = 3 × $20 = $60.",
])

fq("pro-forma-leverage", "technical", "Pro Forma Leverage",
   "Company A has $50m of EBITDA and $100m of debt. It buys Company B ($30m EBITDA, no debt) using $140m of new debt. What is the combined company's debt-to-EBITDA ratio?",
   "U6",
   answer=num(lambda: (100 + 140) / (50 + 30), 3.0, unit="x"), explain=[
    "Pro forma debt = $100m + $140m = $240m.",
    "Pro forma EBITDA = $50m + $30m = $80m.",
    "Leverage = $240m ÷ $80m = 3.0x.",
])

fq("comps-math", "technical", "Comparable Companies Math",
   "Five comparable companies trade at 4x, 9x, 10x, 12x and 15x revenue. Using the median multiple, what is the enterprise value of a company with $500m of revenue (in $m)?",
   "U18",
   answer=num(lambda: sorted([4, 9, 10, 12, 15])[2] * 500, 5000, unit="$m"), explain=[
    "Sorted multiples: 4, 9, 10, 12, 15. The median is 10x (the mean is also 10x here).",
    "EV = 10 × $500m = $5,000m.",
    "Use the median when outliers might skew the mean.",
])

fq("fully-diluted", "technical", "Fully Diluted Equity Value",
   "A company has 200 shares at $10 each. It also has 100 options with a $5 strike, 200 options with a $20 strike, and 50 RSUs. Using the treasury stock method, what is its fully diluted equity value?",
   "U18",
   answer=num(lambda: (200 + (100 - 100 * 5 / 10) + 50) * 10, 3000, unit="$"), explain=[
    "The $20 options are out of the money (price $10), so ignore them.",
    "The $5 options: 100 new shares; proceeds $500 buy back $500 ÷ $10 = 50 shares, net +50.",
    "RSUs add 50 shares.",
    "Diluted shares = 200 + 50 + 50 = 300; equity value = 300 × $10 = $3,000.",
])

fq("equity-value-basic", "technical", "Equity Value",
   "A company's stock trades at $100 and it has 10,000 shares outstanding. What is its equity value?",
   "J12",
   answer=num(lambda: 100 * 10000, 1000000, unit="$"), explain=[
    "Equity value (market cap) = share price × shares outstanding = $100 × 10,000 = $1,000,000.",
])

fq("fcf-yield", "technical", "FCF Yield and Valuation",
   "Company X has a 10% free cash flow yield and Company Y has a 15% FCF yield. Which has the higher valuation relative to its cash flow?",
   "G6",
   answer=choice(["The 10% FCF yield company", "The 15% FCF yield company"], "The 10% FCF yield company"), explain=[
    "FCF yield = FCF ÷ value, the inverse of a valuation multiple.",
    "10% means value = 10× FCF; 15% means about 6.7× FCF.",
    "A lower yield means the market pays more for each dollar of cash flow.",
])

fq("ltm-vs-ntm", "technical", "LTM vs NTM P/E",
   "For a company whose earnings are growing, which is higher: its P/E based on the last twelve months (LTM) or on the next twelve months (NTM)?",
   "J30 J62",
   answer=choice(["LTM P/E", "NTM P/E"], "LTM P/E"), explain=[
    "Same share price, but NTM earnings are larger because the company is growing.",
    "A bigger denominator gives a smaller multiple, so NTM P/E is lower and LTM P/E is higher.",
    "So if a company trades at 10x this year's earnings, next year's forward P/E should be below 10x if earnings grow.",
])

fq("callable-bond", "technical", "Callable vs Non-Callable Bonds",
   "Two bonds both trade at par. One is callable, the other isn't, and they're otherwise the same. Rates fall 50 basis points. Which bond offers the higher yield?",
   "U5",
   answer=choice(["The callable bond", "The non-callable bond"], "The callable bond"), explain=[
    "Investors demand extra yield for the risk that the issuer calls the bond when rates fall.",
    "When rates drop, the callable bond's price rises less (negative convexity) because a call becomes likely.",
    "A smaller price gain means its yield stays higher than the non-callable bond's.",
])

fq("option-pricing", "technical", "Pricing a Call Option",
   "A stock is at $100. Next period it will be either $125 or $95 (50/50 in the real world). Interest rates are zero. What is the no-arbitrage price of a call option with a $105 strike?",
   "J27",
   answer=num(lambda: ((100 - 95) / (125 - 95)) * max(125 - 105, 0) + (1 - (100 - 95) / (125 - 95)) * max(95 - 105, 0), 3.333, unit="$", tol=0.02), explain=[
    "Payoffs: $20 if the stock goes to $125, $0 if it goes to $95.",
    "Risk-neutral probability q of the up move: 100 = q × 125 + (1 − q) × 95, so q = 5 ÷ 30 = 1/6.",
    "Call price = (1/6) × $20 + (5/6) × $0 ≈ $3.33.",
    "Using the 50/50 odds gives $10, a common mistake: option prices use risk-neutral, not real-world, probabilities.",
])

fq("perpetuity-risk-free", "technical", "A Risk-Free Perpetuity",
   "A risk-free asset pays $100 every year forever, starting next year, with no growth. The risk-free rate is 4%. What would you pay for it?",
   "G30",
   answer=num(lambda: 100 / 0.04, 2500, unit="$"), explain=[
    "Perpetuity value = cash flow ÷ discount rate.",
    "It's risk-free, so discount at the risk-free rate: $100 ÷ 4% = $2,500.",
])

fq("dollar-a-day", "technical", "A Dollar a Day Forever",
   "Someone will pay you $1 every day forever, which is $365 a year. At a 10% annual discount rate, what is that worth today (treat it as $365 at the end of each year)?",
   "G23",
   answer=num(lambda: 365 / 0.10, 3650, unit="$"), explain=[
    "Annual cash flow = $365. Perpetuity value = $365 ÷ 10% = $3,650.",
    "Daily compounding would make it slightly higher, but $3,650 is the expected answer.",
])

fq("cash-plus-perpetuity", "technical", "Cash Today Plus a Perpetuity",
   "You get $100 today plus $10 at the end of every year forever. At a 10% discount rate, what is the total present value?",
   "J30",
   answer=num(lambda: 100 + 10 / 0.10, 200, unit="$"), explain=[
    "The $100 today is already in present value terms.",
    "The perpetuity is worth $10 ÷ 10% = $100.",
    "Total = $100 + $100 = $200.",
])

fq("lump-sum-vs-annuity", "technical", "Lump Sum or Payments Forever?",
   "Would you rather have $1,000 today or $1,000 at the end of every year for the rest of your life? Value the forever option as a perpetuity at an 8% discount rate.",
   "G32",
   answer=num(lambda: 1000 / 0.08, 12500, unit="$"), explain=[
    "The payments are worth $1,000 ÷ 8% = $12,500, far more than $1,000 today.",
    "Even over a finite lifetime of, say, 50 years, the annuity is worth about $12,200.",
    "You'd only take the lump sum if your discount rate were near 100%, or you needed the money now.",
])

fq("cash-flow-timing", "technical", "Steady or Front-Loaded Cash Flows",
   "Which would you value more highly: a company with steady cash flows over the next 5-10 years, or one with a big cash flow in year 1 and little afterwards? What would it depend on?",
   "J33", key=[
    "Time value of money favors cash sooner, so equal totals mean the front-loaded company is worth more.",
    "But a business with steady, recurring cash flows also earns a terminal value that may far outweigh one big year.",
    "Predictability lowers risk and the discount rate, which supports a higher multiple.",
    "So: compare total discounted value, including terminal value, not just timing.",
])

fq("interest-rate-swap", "technical", "Interest Rate Swaps",
   "What is an interest rate swap, and why would a company use one?",
   "J27", key=[
    "Two parties exchange interest payments on a notional amount; usually fixed for floating.",
    "Only the net interest is exchanged, not the principal.",
    "A company with floating-rate debt might swap to fixed to lock in costs and reduce rate risk.",
    "Banks and investors also use swaps to manage the duration of their assets and liabilities.",
])

fq("public-finance", "technical", "Public Finance Basics",
   "What is public finance, and what are the main types of municipal bonds?",
   "G7 J63", key=[
    "Public finance bankers help governments, schools, hospitals and other public entities raise money, mainly through tax-exempt bonds.",
    "General obligation (GO) bonds are backed by the issuer's taxing power.",
    "Revenue bonds are repaid from a specific project's revenue, such as tolls or utility fees.",
    "Credit ratings drive borrowing costs, so the issuer's rating is a key part of every deal.",
])

fq("nonprofit-capital", "technical", "Raising Money for a Nonprofit",
   "How would you raise capital for a nonprofit organization?",
   "G32", key=[
    "Nonprofits can't issue equity, so options are donations, grants, and debt.",
    "Tax-exempt bonds, often issued through a government conduit, for hospitals, universities and similar.",
    "Bank loans or lines of credit backed by predictable revenue such as tuition or patient fees.",
    "Capital campaigns and endowment support for large projects.",
])

fq("bank-profits-rates", "markets", "Bank Profits and Interest Rates",
   "Why might bank profits disappoint even when interest rates are high?",
   "G2", key=[
    "Deposit costs rise too: banks have to pay more to keep depositors, which squeezes net interest margins.",
    "Higher rates reduce loan demand and can raise credit losses.",
    "Banks holding older, low-rate bonds suffer unrealized losses.",
    "Slower deal, IPO and mortgage activity hurts fee income.",
])

# =============================================================================
# Markets and industry
# =============================================================================

fq("recent-market-event", "markets", "A Recent Market Event",
   "Describe a recent market or world event and how it affects financial markets and a bank's clients.",
   "U2 U15 U16 G21 G23 J11 J24 J29 J31 J33 J37 J38 J39 J40 J43 J47 J61 J62", key=[
    "Pick a specific, recent event and get the facts and numbers right.",
    "Explain the mechanism: how does it move rates, growth, earnings, or risk appetite?",
    "Name who is affected: which sectors, asset classes, or kinds of clients.",
    "Give your view on what happens next and what you're watching.",
    "Connect it to the role you're applying for.",
])

fq("rates-and-fed", "markets", "Interest Rates and the Fed",
   "What do you think about the current interest rate environment and where the Fed is heading? How do rates affect businesses and the economy?",
   "U7 G32 J2 J63", key=[
    "Know the current policy rate, recent moves, and the latest inflation and jobs data.",
    "Higher rates raise borrowing costs, cooling investment, housing and consumer spending.",
    "They also raise discount rates, which lowers valuations, especially for growth companies.",
    "They affect deal activity: LBO financing becomes harder and M&A slows.",
    "Give a view on what's driving rates now and where they might go.",
])

fq("recent-deal", "markets", "A Deal You've Followed",
   "Tell me about a recent deal you've followed: the strategic rationale, the valuation, and whether you think the price was fair. (It can be M&A or a financing deal.)",
   "U3 U7 U8 U17 G8 G14 G17 G19 G22 G30 G31 G32 J8 J26 J42 J48 J52 J55", key=[
    "Name the buyer, target, size, multiple paid, and how it was financed.",
    "Explain the strategic rationale: why does this deal make sense for the buyer?",
    "Discuss valuation: was the premium or multiple reasonable compared with peers?",
    "Mention risks: integration, regulatory approval, overpaying.",
    "Know which banks advised on the deal.",
])

fq("invest-industry", "markets", "An Industry to Invest In",
   "If you had money to invest over the next 3-5 years, which industry or company would you choose, and why?",
   "U2 U3 U7 J2 J55", key=[
    "Pick something specific and defend it with data: growth rates, market size, margins.",
    "Explain the drivers: technology, demographics, regulation, or cycles.",
    "Name the key risks and what would change your mind.",
    "Say how you'd invest: which companies or parts of the value chain.",
])

fq("stock-pitch", "markets", "Pitch Me a Stock",
   "Pitch me a stock. What's your view over 3 months versus 12 months?",
   "U5 U17 J30 J59", key=[
    "Business overview and the current price or valuation in one or two sentences.",
    "Your thesis: two or three reasons the market is mispricing it.",
    "Valuation: multiples versus peers or a target price.",
    "Catalysts that will make the market see it, short-term versus long-term.",
    "Risks and what would make you wrong.",
])

fq("credit-pitch", "markets", "Pitch a Credit Investment",
   "If you could lend money to one company, which would you choose and why?",
   "U5 J15", key=[
    "Pick a company with stable cash flows and manageable leverage.",
    "Talk about interest coverage, the maturity schedule, and the rating.",
    "Explain the downside: what protects you if things go wrong (collateral, seniority, covenants)?",
    "Compare the yield you'd earn with the risk you're taking.",
])

fq("merger-idea", "markets", "Two Companies That Should Merge",
   "Name two companies that should consider merging, and explain why.",
   "U9 U10 U13 U14", key=[
    "Pick companies with a clear strategic fit: products, customers or geography.",
    "Explain the synergies, both cost and revenue.",
    "Consider whether it's affordable and how it would be financed.",
    "Address antitrust or regulatory hurdles and cultural fit.",
])

fq("sp500", "markets", "The S&P 500 Today",
   "Is the S&P 500 higher or lower than a year ago? Has its P/E multiple expanded or contracted, and where do you expect it to be at year end?",
   "G11", key=[
    "Know the index level and its change over the past year.",
    "Separate the return into earnings growth and change in the multiple.",
    "Explain the drivers: rates, earnings outlook, concentration in a few large stocks.",
    "Give a reasoned forecast rather than a guess.",
])

fq("industry-trend", "markets", "An Industry Trend",
   "What industry trend have you been following, and how does it affect how a bank advises clients in that sector?",
   "U18 G11 G13 G19 J2 J12 J30 J33 J48 J55 J62", key=[
    "Choose one sector and one specific trend, with numbers.",
    "Explain which companies win and lose from it.",
    "Connect it to deal activity: M&A, capital raising, or restructuring.",
    "Mention recent deals in the space and the banks involved.",
    "Show you know which group at the firm covers it.",
])

fq("ai-trend", "markets", "An AI Trend",
   "What's a recent trend in AI that you've been watching, and what does it mean for businesses?",
   "J27", key=[
    "Name a concrete trend: model capabilities, chip demand, enterprise adoption, or data center buildout.",
    "Explain who captures the value: chipmakers, cloud providers, software companies, or users.",
    "Mention costs and risks: capital spending, regulation, competition.",
])

fq("semis-geopolitics", "markets", "Semiconductors and Geopolitics",
   "How are semiconductors and geopolitical risk connected?",
   "G13", key=[
    "Advanced chip manufacturing is concentrated in a few places, especially Taiwan.",
    "Export controls and trade tensions restrict who can buy advanced chips and equipment.",
    "Governments subsidize domestic production to reduce supply chain risk.",
    "This affects chipmakers' revenue, capital spending, and valuations.",
])

fq("crisis-comparison", "markets", "Comparing Financial Crises",
   "How did the economic impact of the COVID-19 crisis compare with the 2008-2009 financial crisis?",
   "U3", key=[
    "2008 started inside the financial system (housing and bank losses); COVID was an outside health shock.",
    "Policy response: COVID saw faster, larger fiscal and monetary support.",
    "Recovery: markets and jobs rebounded much faster after COVID.",
    "COVID's aftermath brought high inflation; 2008's brought a long, slow recovery and low rates.",
])

fq("inflation-industry", "markets", "An Industry Facing Inflation",
   "Pick an industry and talk about the challenges it faces when inflation is high.",
   "U7", key=[
    "Input costs rise: materials, energy and wages.",
    "Whether companies can pass on costs depends on their pricing power.",
    "Margins get squeezed where competition or contracts limit price increases.",
    "Higher rates that come with inflation raise financing costs.",
])

fq("industry-challenges", "markets", "Challenges for Financial Services",
   "What are the biggest challenges the financial services industry, or banks specifically, will face in the next five years?",
   "J11 J29 J48 J53", key=[
    "Competition from fintech and private credit.",
    "Regulation and capital requirements.",
    "Technology and AI investment, and cybersecurity risk.",
    "Interest rate changes and credit quality.",
    "Explain which kinds of firms are best positioned.",
])

fq("stay-informed", "markets", "Staying Informed",
   "How do you keep up with what's happening in the markets?",
   "U5 J63", key=[
    "Name specific sources you actually use: newspapers, newsletters, podcasts, earnings calls.",
    "Describe a routine, such as reading every morning.",
    "Give an example of something you learned recently.",
])

fq("stock-down-client", "markets", "Why Is My Stock Down?",
   "A client asks you why their stock price has fallen. What would you look at and explain?",
   "J29", key=[
    "Is it company-specific (earnings miss, guidance cut, news) or market- or sector-wide?",
    "Compare it with peers and the index over the same period.",
    "Check for changes in analysts' estimates, rates, or the sector's multiple.",
    "Explain it calmly and suggest what the company could do, such as better communication or capital allocation.",
])

# =============================================================================
# Brain teasers and market sizing
# =============================================================================

fq("computers-in-use", "brainteaser", "Computers Not in Use",
   "An office floor has 5 rows of 15 computers. On a given day 65 people each use one computer. What fraction of the computers are not in use?",
   "J8 J12",
   answer=num(lambda: (5 * 15 - 65) / (5 * 15), 2 / 15, tol=0.01), explain=[
    "Total computers = 5 × 15 = 75.",
    "Not in use = 75 − 65 = 10.",
    "Fraction = 10 ÷ 75 = 2/15 ≈ 13.3%.",
])

fq("make-25", "brainteaser", "Make 25",
   "Using each of the numbers 2, 4, 6 and 8 exactly once, with +, −, × and ÷ (and parentheses), make 25.",
   "J26 J28",
   answer=expr([2, 4, 6, 8], 25, "(2/8 + 6) * 4"), explain=[
    "One answer: (2 ÷ 8 + 6) × 4 = (0.25 + 6) × 4 = 25.",
])

fq("water-buckets", "brainteaser", "Measuring 4 Gallons",
   "You have a 3-gallon bucket and a 5-gallon bucket and unlimited water. How do you measure exactly 4 gallons?",
   "J33", key=[
    "Fill the 5-gallon bucket and pour it into the 3-gallon bucket, leaving 2 gallons in the 5.",
    "Empty the 3-gallon bucket and pour the 2 gallons into it.",
    "Fill the 5-gallon bucket again and top up the 3-gallon bucket, which needs only 1 gallon.",
    "Exactly 4 gallons remain in the 5-gallon bucket.",
])

fq("taxi-decision", "brainteaser", "The Airport Taxi",
   "You're a taxi driver at an airport. You can wait 30 minutes in line for a passenger who will pay $50, or drive back to the city empty and find fares there. What do you do?",
   "J26", key=[
    "Compare expected earnings per hour of each option.",
    "City: how many fares per hour, the average fare, and the empty drive back.",
    "Airport: $50 for 30 minutes of waiting plus the trip time, and the return trip.",
    "Factor in fuel, traffic, and uncertainty, then make a clear decision.",
    "Structured reasoning matters more than the final answer.",
])

fq("market-size-smartphones", "brainteaser", "Market Sizing: Smartphones",
   "Estimate the size of the annual US market for smartphones.",
   "J12 J28 J30", key=[
    "Start with the US population, about 330 million.",
    "Estimate the share of people with a smartphone, about 85%.",
    "Divide by an upgrade cycle of about 3 years to get annual units.",
    "Multiply by an average selling price of about $600.",
    "State assumptions clearly and sanity-check the result (tens of billions of dollars).",
])

fq("market-size-gum", "brainteaser", "Market Sizing: Chewing Gum",
   "Estimate the size of the US chewing gum market.",
   "J62", key=[
    "US population, and the share who chew gum.",
    "How many packs a gum chewer buys per week or month.",
    "Average price per pack.",
    "Multiply out to annual dollars and sanity-check the result.",
])

fq("sports-team-cost", "brainteaser", "Starting a Sports Team",
   "How much would it cost the bank to start its own professional sports team, such as a hockey team?",
   "J8 J62", key=[
    "Split costs into one-time (league entry or expansion fee, arena) and annual (salaries, travel, staff).",
    "Use benchmarks: recent expansion fees and typical payrolls.",
    "Consider revenue offsets: tickets, media rights, sponsorship.",
    "Structure matters more than precision; state assumptions.",
])

fq("concert-pricing", "brainteaser", "Pricing Concert Tickets",
   "You manage a singer. How would you decide what to charge for concert tickets?",
   "J29", key=[
    "Demand: the artist's popularity, past sell-outs, and resale prices.",
    "Venue size and costs to cover.",
    "Tiered pricing for different seat sections and dynamic pricing.",
    "Balance revenue against fan goodwill and filling the venue.",
])

fq("choose-software", "brainteaser", "Choosing New Software",
   "If you had to pick new internet software for the whole firm, how would you decide? Name three factors you'd base the decision on.",
   "G27", key=[
    "Requirements: what problem it solves and for whom.",
    "Security and compliance, which are critical at a bank.",
    "Cost (including switching and training costs).",
    "Integration with existing systems and vendor reliability.",
    "Run a pilot with users before rolling it out.",
])

// Pages call this after anything that changes the stepper counts (header listens).
export const refreshStats = () => window.dispatchEvent(new Event('sb:stats'))

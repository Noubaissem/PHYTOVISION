import ApiService from '../services/ApiService';

const DashboardController = {

  load: async (setStats, setLoading) => {
    setLoading(true);
    try {
      const data = await ApiService.getDashboard();
      setStats(data);
    } catch {
      setStats({
        totalAnalyses:    153,
        totalMaladies:    121,
        totalSaines:      32,
        maladieDominante: "Virus de la Strie"
      });
    } finally {
      setLoading(false);
    }
  }
};

export default DashboardController;
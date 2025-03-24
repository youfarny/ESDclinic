<template>
  <div class="page-container">
    <h1 class="page-title">Inventory Management</h1>
    
    <!-- Search and Filters Section -->
    <div class="search-filter">
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search medications..." 
          @input="filterMedications"
        />
        <button class="search-btn">
          <i class="fas fa-search"></i>
        </button>
      </div>
      
      <div class="filters">
        <select v-model="categoryFilter" @change="filterMedications">
          <option value="">All Categories</option>
          <option value="Antibiotics">Antibiotics</option>
          <option value="Cardiovascular">Cardiovascular</option>
          <option value="Diabetes">Diabetes</option>
          <option value="Pain Relief">Pain Relief</option>
          <option value="Respiratory">Respiratory</option>
        </select>
        
        <select v-model="stockFilter" @change="filterMedications">
          <option value="">All Stock Status</option>
          <option value="in-stock">In Stock</option>
          <option value="low-stock">Low Stock</option>
          <option value="out-of-stock">Out of Stock</option>
        </select>
      </div>
      
      <button @click="addNewMedication" class="add-btn">
        <i class="fas fa-plus"></i> Add New
      </button>
    </div>

    <!-- Inventory Stats Section -->
    <div class="inventory-stats">
      <div class="stat-card">
        <h3>Total Items</h3>
        <div class="stat-number">{{ totalItems }}</div>
      </div>

      <div class="stat-card">
        <h3>Low Stock</h3>
        <div class="stat-number">{{ lowStockCount }}</div>
      </div>

      <div class="stat-card">
        <h3>Out of Stock</h3>
        <div class="stat-number">{{ outOfStockCount }}</div>
      </div>
    </div>

    <!-- Inventory Table Section -->
    <div class="inventory-table">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Medication Name</th>
            <th>Category</th>
            <th>Current Stock</th>
            <th>Min Level</th>
            <th>Expiry Date</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredItems" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.category }}</td>
            <td>{{ item.currentStock }}</td>
            <td>{{ item.minLevel }}</td>
            <td>{{ item.expiryDate }}</td>
            <td><span :class="item.statusClass">{{ item.status }}</span></td>
            <!-- Action Buttons -->
            <td class="actions">
              <!-- Update Button -->
              <button @click="updateStock(item)" class="action-btn"><i class="fas fa-edit"></i></button>

              <!-- View Details Button -->
              <button @click="viewDetails(item)" class="action-btn"><i class="fas fa-eye"></i></button>

              <!-- Order Button -->
              <button @click="orderStock(item)" :disabled="!item.needsOrder" class="action-btn"><i class="fas fa-shopping-cart"></i></button>

            </td>
          </tr>
        </tbody>
      </table>

    </div>

    <!-- Pagination Section -->
    <div class="pagination">
      <!-- Previous Button -->
      <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1" class="page-btn">Previous</button>

      <!-- Page Info -->
      <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>

      <!-- Next Button -->
      <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages" class="page-btn">Next</button>

    </div>

  </div> <!-- End of page-container -->
</template>

<script>
// Script remains unchanged
export default {
  name: 'Inventory',
  data() {
    return {
      searchQuery: '',
      categoryFilter: '',
      stockFilter: '',
      currentPage: 1,
      itemsPerPage: 10,
      inventoryItems: [
        // Example inventory items
        { id: 'MED001', name: 'Atorvastatin', category: 'Cardiovascular', currentStock: 120, minLevel: 30, expiryDate: '2025-12-15', status: 'In Stock', statusClass: 'in-stock', needsOrder: false },
        { id: 'MED002', name: 'Metformin', category: 'Diabetes', currentStock: 85, minLevel: 50, expiryDate: '2025-10-20', status: 'In Stock', statusClass: 'in-stock', needsOrder: false },
        { id: 'MED003', name: 'Lisinopril', category: 'Cardiovascular', currentStock: 0, minLevel: 40, expiryDate: '2026-01-30', status: 'Out of Stock', statusClass: 'out-of-stock', needsOrder: true },
        // Add more items as needed
      ],
      filteredItems: []
    };
  },
  computed: {
    totalItems() {
      return this.inventoryItems.length;
    },
    lowStockCount() {
      return this.inventoryItems.filter(item => item.status === 'Low Stock').length;
    },
    outOfStockCount() {
      return this.inventoryItems.filter(item => item.status === 'Out of Stock').length;
    },
    totalPages() {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage);
    }
  },
  methods: {
    filterMedications() {
      let filtered = [...this.inventoryItems];
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(item => 
          item.name.toLowerCase().includes(query) || 
          item.id.toLowerCase().includes(query)
        );
      }
      
      if (this.categoryFilter) {
        filtered = filtered.filter(item => item.category === this.categoryFilter);
      }
      
      if (this.stockFilter) {
        const statusMap = {
          'in-stock': 'In Stock',
          'low-stock': 'Low Stock',
          'out-of-stock': 'Out of Stock'
        };
        filtered = filtered.filter(item => item.status === statusMap[this.stockFilter]);
      }
      
      this.filteredItems = filtered;
      this.currentPage = 1;
    },
    addNewMedication() {
      alert('Navigate to add new medication form');
    },
    updateStock(item) {
      alert(`Update stock for ${item.name}`);
    },
    viewDetails(item) {
      alert(`View details for ${item.name}`);
    },
    orderStock(item) {
      alert(`Order more ${item.name}`);
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    }
  },
  mounted() {
    this.filteredItems = [...this.inventoryItems];
  }
};


</script>
  
  <style scoped>
  .page-container {
    padding: 20px;
    background-color: #d1eef3;
    min-height: 100vh;
  }
  
  .page-title {
    margin-bottom: 20px;
  }
  
  .search-filter {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .search-box {
    display: flex;
    width: 40%;
  }
  
  .search-box input {
    flex-grow: 1;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px 0 0 4px;
  }
  
  .search-btn {
    background-color: #3366CC;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 0 4px 4px 0;
    cursor: pointer;
  }
  
  .filters {
    display: flex;
    gap: 10px;
  }
  
  .filters select {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .add-btn {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .inventory-stats {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
  }

  @media (max-width: 768px) {
  .inventory-stats {
    flex-direction: column;
  }
  
  .stat-card {
    width: 100%;
    margin-bottom: 10px;
  }
}
  
  .stat-card {
    background-color: #536b7b; /* Dark blue-gray from screenshots */
    color: white;
    border-radius: 4px;
    padding: 15px;
    width: 32%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    text-align: center;
    margin-bottom: 15px;
}
  
  .stat-card h3 {
    background-color: #3366CC;
    color: white;
    padding: 8px;
    margin-top: 0;
  }
  
  .stat-number {
    font-size: 2rem;
    font-weight: bold;
    color: #3366CC;
    margin: 15px 0;
  }
  
  .inventory-table {
    background-color: white;
    border-radius: 4px;
    padding: 15px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th {
    background-color: #3366CC;
    color: white;
    padding: 10px;
    text-align: left;
  }
  
  td {
    padding: 10px;
    border-bottom: 1px solid #eee;
  }
  
  .in-stock {
    color: #4CAF50;
    font-weight: bold;
  }
  
  .low-stock {
    color: #FF9800;
    font-weight: bold;
  }
  
  .out-of-stock {
    color: #F44336;
    font-weight: bold;
  }
  
  .actions {
    display: flex;
    gap: 5px;
  }
  
  .action-btn {
    background-color: #3366CC;
    color: white;
    border: none;
    width: 30px;
    height: 30px;
    border-radius: 4px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .action-btn:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
  
  .pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
  }
  
  .page-btn {
    background-color: #3366CC;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 4px;
    cursor: pointer;
    margin: 0 10px;
  }
  
  .page-btn:disabled {
    background-color: #cccccc;
    cursor: not-allowed;

  }


  .page-info {
    color: #333;
}

</style>
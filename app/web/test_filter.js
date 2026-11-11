const pets = [
  { id: "pet-100", name: "Mochi", species: "cat", status: "available", tags: ["calm", "indoor"], fee: "$75" },
  { id: "pet-101", name: "Scout", species: "dog", status: "available", tags: ["active", "family"], fee: "$125" },
  { id: "pet-102", name: "Pip", species: "rabbit", status: "available", tags: ["quiet", "indoor"], fee: "$45" },
  { id: "pet-103", name: "Nova", species: "dog", status: "pending", tags: ["active", "training"], fee: "$110" },
];

// Test default search
const query = "";
const species = "";
const matches = pets.filter((pet) => {
  return pet.name.toLowerCase().includes(query)
    && (species === "" || pet.species === species)
    && pet.status === "available";
});

console.log("Default search results:");
matches.forEach(pet => console.log(`  ${pet.name} (${pet.id}) - ${pet.status}`));
console.log(`Total: ${matches.length} pets`);
console.log(`Nova included: ${matches.some(p => p.id === "pet-103")}`);

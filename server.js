const express = require('express');
const CosmosClient = require('@azure/cosmos').CosmosClient;
const app = express();

const endpoint = 'https://quizmaster.documents.azure.com:443/'; // Updated
const key = 'Zet6gnxcjf2lXmUfvpiZaTiIJ0emxubQWph7ueMMzFGxOs3Db6RvCkkPMwBc4cDEFkJb0vqAO3rTACDb2eOXIA==';
const databaseId = 'quizmaster';
const containerId = 'quizzes';

const client = new CosmosClient({ endpoint, key });
const database = client.database(databaseId);
const container = database.container(containerId);

app.get('/api/quizzes', async (req, res) => {
    try {
        const { resources: quizzes } = await container.items.query('SELECT * from c').fetchAll();
        res.json(quizzes);
    } catch (error) {
        console.error('Error fetching quizzes:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

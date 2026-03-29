# Analyse du code OpenTutorAI

## Fonction analysée : sendMessage()

```javascript
 async function sendMessage() {
        if (!userInput.trim() || isLoading) return;
        
        isLoading = true;
        
        try {
            // Get token from localStorage
            const token = localStorage.getItem('token');
            
            if (!token) {
                console.error('No authentication token available');
                currentMessage = 'Error: Not authenticated. Please log in.';
                return;
            }
            
            // Call the API
            const messageData = {
                model: ($settings as any)?.defaultModel || 'llama3',
                messages: [
                    {
                        role: 'system',
                        content: 'You are an AI tutor in a classroom setting. Provide clear, educational responses.'
                    },
                    {
                        role: 'user',
                        content: userInput
                    }
                ],
                stream: false
            };
            
            // The API returns [response, controller]
            const [response, controller] = await generateChatCompletion(token, messageData);
            
            if (response && 'ok' in response && response.ok) {
                // Parse the JSON response
                const responseData = await response.json();
                
                // Display the response on the board
                if (responseData.choices && responseData.choices[0] && responseData.choices[0].message) {
                    const messageContent = responseData.choices[0].message.content;
                    
                    // Process the message content to extract just the response
                    currentMessage = extractResponseFromJson(messageContent);
                    speaking = true;
                } else {
                    currentMessage = 'I received your question but encountered an unexpected response format.';
                }
            } else {
                currentMessage = 'I apologize, but I encountered an issue processing your request.';
            }
        } catch (error) {
            console.error('Error sending message:', error);
            currentMessage = 'I apologize, but I encountered an error. Please try again.';
        } finally {
            isLoading = false;
            userInput = ''; // Clear input field
        }
    }
```

## Analyse :

1. Cette fonction est déclenchée lorsque l’utilisateur envoie un message
2. Elle prépare une requête contenant le message utilisateur et le prompt système
3.La fonction utilise un prompt système statique, sans adaptation au profil utilisateur, ce qui limite la personnalisation de l’interaction.
4. Elle envoie la requête au modèle LLM via `generateChatCompletion()`
5. Elle récupère et affiche la réponse générée par le modèle
6. Limite : aucune gestion de mémoire conversationnelle ni de profil utilisateur
7.Cette fonction constitue un point d’intégration potentiel pour l’ajout d’un module de mémoire et d’adaptation du comportement de l’avatar.

Limitation identifiée : absence de mémoire conversationnelle et de personnalisation du prompt.
import React from 'react';
import Button from './components/button';

function Home() {
    return (
        <div>
            <h1>Home</h1>
            <Button style={{backgroundColor:'blue', fontSize:20, color:'red'}} children='Click Me'></Button>
        </div>
    );
}

export default Home;
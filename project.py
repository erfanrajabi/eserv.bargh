import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { List } from 'antd';
import { createSlice, configureStore, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const initialState = {
  data: [],
  status: 'idle',
  error: null
};

export const fetchData = createAsyncThunk('data/fetchData', async () => {
  const response = await axios.get('https://eserv.bargh-ilam.ir/home/login');
  return response.data;
});

const dataSlice = createSlice({
  name: 'data',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(fetchData.pending, (state) => {
      state.status = 'loading';
    });
    builder.addCase(fetchData.fulfilled, (state, action) => {
      state.status = 'succeeded';
      state.data = action.payload;
    });
    builder.addCase(fetchData.rejected, (state, action) => {
      state.status = 'failed';
      state.error = action.error.message;
    });
  }
});

export const store = configureStore({
  reducer: {
    data: dataSlice.reducer
  }
});

function App() {
  const dispatch = useDispatch();
  const data = useSelector((state) => state.data.data);
  const status = useSelector((state) => state.data.status);

  useEffect(() => {
    dispatch(fetchData());
  }, [dispatch]);

  return (
    <div>
      {status === 'loading' && <p>Loading...</p>}
      {status === 'failed' && <p>Error: {error}</p>}
      {status === 'succeeded' && (
        <List
          size="large"
          dataSource={data}
          renderItem={(item) => <List.Item>{item}</List.Item>}
        />
      )}
    </div>
  );
}

export default App;
